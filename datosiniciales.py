import numpy as np

# --- CONFIGURACIÓN DEL SISTEMA ---
box_size = 50.0  # Tamaño de la caja (unidades LJ)
r_vesicle = 15.0 # Radio de la vesícula
n_lipids = 1200  # Número aproximado de lípidos (puedes subirlo a 2500)
drug_particles = 100 # Cantidad de perlas de fármaco en el centro

# Tipos de átomos (Mapping 4:1 del artículo)
# 1:W, 2:Q0, 3:Qa, 4:Na, 5:C, 6:Drug

def generate_vesicle():
    atoms = []
    bonds = []
    
    atom_id = 1
    mol_id = 1
    
    # 1. GENERAR LÍPIDOS (Orientación radial)
    for i in range(n_lipids):
        # Decidir si va en capa interna o externa
        is_outer = np.random.random() > 0.4
        r = r_vesicle + (1.5 if is_outer else -1.5)
        
        # Coordenadas esféricas aleatorias
        phi = np.random.uniform(0, 2*np.pi)
        costheta = np.random.uniform(-1, 1)
        theta = np.arccos(costheta)
        
        # Vector unitario de dirección
        dx = np.sin(theta) * np.cos(phi)
        dy = np.sin(theta) * np.sin(phi)
        dz = np.cos(theta)
        
        # Dirección de la cabeza (hacia afuera si es outer, hacia adentro si es inner)
        dir_mult = 1.0 if is_outer else -1.0
        
        # Crear perlas del lípido (Q0-Qa-Na y dos colas C4)
        # Simplificación de la estructura para el data file:
        # Q0(2), Qa(3), Na(4), C(5), C(5), C(5), C(5) ...
        
        # Cabeza y cuello
        positions = [
            (r + 2.0*dir_mult) * np.array([dx, dy, dz]), # Q0
            (r + 1.5*dir_mult) * np.array([dx, dy, dz]), # Qa
            (r + 1.0*dir_mult) * np.array([dx, dy, dz]), # Na
        ]
        types = [2, 3, 4]
        
        # Colas (2 colas de 4 perlas C)
        for _ in range(2):
            for c_step in range(4):
                pos = (r - (c_step*0.5)*dir_mult) * np.array([dx, dy, dz])
                positions.append(pos)
                types.append(5)
        
        # Guardar átomos y crear enlaces
        start_id = atom_id
        for p, t in zip(positions, types):
            # Centrar en la caja
            p += box_size / 2.0
            atoms.append(f"{atom_id} {mol_id} {t} 0.0 {p[0]:.3f} {p[1]:.3f} {p[2]:.3f}")
            atom_id += 1
        
        # Enlaces simples lineales para el ejemplo (Q0-Qa, Qa-Na, Na-C1...)
        for b in range(len(positions)-1):
            bonds.append(f"{len(bonds)+1} 1 {start_id+b} {start_id+b+1}")
            
        mol_id += 1

    # 2. GENERAR FÁRMACO EN EL CENTRO
    for _ in range(drug_particles):
        # Posición aleatoria en una esfera pequeña central (r=5)
        r_f = np.random.uniform(0, 5.0)
        phi = np.random.uniform(0, 2*np.pi)
        costheta = np.random.uniform(-1, 1)
        theta = np.arccos(costheta)
        px = r_f * np.sin(theta) * np.cos(phi) + box_size/2
        py = r_f * np.sin(theta) * np.sin(phi) + box_size/2
        pz = r_f * np.cos(theta) + box_size/2
        atoms.append(f"{atom_id} {mol_id} 6 0.0 {px:.3f} {py:.3f} {pz:.3f}")
        atom_id += 1
        mol_id += 1

    # 3. ESCRIBIR ARCHIVO DATA
    with open("posiciones.data", "w") as f:
        f.write("LAMMPS Vesicle Data File\n\n")
        f.write(f"{len(atoms)} atoms\n")
        f.write(f"{len(bonds)} bonds\n\n")
        f.write("6 atom types\n")
        f.write("1 bond types\n\n")
        f.write(f"0.0 {box_size} xlo xhi\n")
        f.write(f"0.0 {box_size} ylo yhi\n")
        f.write(f"0.0 {box_size} zlo zhi\n\n")
        f.write("Atoms\n\n")
        for a in atoms: f.write(a + "\n")
        f.write("\nBonds\n\n")
        for b in bonds: f.write(b + "\n")

print("Archivo data.vesicle generado exitosamente.")
generate_vesicle()
