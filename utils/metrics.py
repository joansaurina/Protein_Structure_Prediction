import json
import numpy as np
import os
import re
import pymol
import subprocess
import pandas as pd
import uuid

def process_full_data_file_alphafold(file_path, unique_id):
    """
    Process a single JSON file ending in '_full_data.json' or '_full_data_0.json'.
    Compute and return the mean of 'atom_plddts' and 'pae' for the specified file.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extract arrays
    atom_plddts = data.get("atom_plddts", [])
    pae = data.get("pae", [])

    # Compute means
    atom_plddts_mean = np.mean(atom_plddts) if atom_plddts else float('nan')
    pae_mean = np.mean(pae) if pae else float('nan')

    # Format means with comma as decimal separator
    atom_plddts_mean_str = f"{atom_plddts_mean:,.2f}".replace(",", "temp").replace(".", ",").replace("temp", ".")
    pae_mean_str = f"{pae_mean:,.2f}".replace(",", "temp").replace(".", ",").replace("temp", ".")

    return unique_id, atom_plddts_mean_str, pae_mean_str

def process_full_data_file_protenix(file_path, unique_id):
    """
    Process a single JSON file ending in '_full_data.json' or '_full_data_0.json'.
    Compute and return the mean of 'atom_plddts' and 'pae' for the specified file.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extract arrays
    atom_plddts = data.get("atom_plddt", [])
    pae = data.get("token_pair_pae", [])

    # Compute means
    atom_plddts_mean = np.mean(atom_plddts) if atom_plddts else float('nan')
    pae_mean = np.mean(pae) if pae else float('nan')

    # Format means with comma as decimal separator
    atom_plddts_mean_str = f"{atom_plddts_mean:,.2f}".replace(",", "temp").replace(".", ",").replace("temp", ".")
    pae_mean_str = f"{pae_mean:,.2f}".replace(",", "temp").replace(".", ",").replace("temp", ".")

    return unique_id, atom_plddts_mean_str, pae_mean_str

def process_pae_npy(file_path):
    """
    Process a .npy file to extract the mean PAE value from a 2D array.
    """
    # Load the .npy file
    pae_data = np.load(file_path)
    
    # Flatten the 2D array and compute the mean
    pae_mean = np.mean(pae_data) if pae_data.size > 0 else float('nan')
    
    # Format the mean with comma as the decimal separator
    pae_mean_str = f"{pae_mean:,.2f}".replace(",", "temp").replace(".", ",").replace("temp", ".")
    
    return pae_mean_str

def process_chai_json(file_path):
    """
    Process a JSON file for Chai to extract relevant metrics like PAE.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    ptm = data.get("ptm", float('nan'))
    ptm_str = f"{ptm:,.2f}".replace(",", "temp").replace(".", ",").replace("temp", ".")
    return ptm_str

def process_summary_confidences_file(file_path):
    """
    Process a single JSON file ending in '_summary.json' or '_summary_confidences_0.json'.
    Extract and return the 'ptm' and 'iptm' scores for the specified file.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extract 'ptm' and 'iptm' scores
    ptm_score = data.get("ptm", float('nan'))

    # Format scores with comma as decimal separator
    ptm_score_str = f"{ptm_score:,.2f}".replace(",", "temp").replace(".", ",").replace("temp", ".") if ptm_score is not None else "N/A"

    return ptm_score_str

def convert_cif_to_pdb(cif_file, pdb_file):
    """
    Converts a CIF file to PDB format using OpenBabel.
    """
    subprocess.run(['obabel', cif_file, '-O', pdb_file], check=True)
    #print(f"Converted CIF to PDB: {cif_file} -> {pdb_file}")

def pymol_rmsd(structure1, structure2, graph=False):
    pymol.finish_launching(['pymol', '-c'])

    structure1 = os.path.abspath(structure1)
    structure2 = os.path.abspath(structure2)

    # Get the file extensions
    ext1 = structure1.split('.')[-1].lower()
    ext2 = structure2.split('.')[-1].lower()

    # Check if the file types are different and convert CIF to PDB if needed
    if ext1 != ext2:
        if ext1 == 'cif' and ext2 == 'pdb':
            #print(f"File formats are different. Converting {structure1} from CIF to PDB.")
            structure1_pdb = os.path.splitext(structure1)[0] + '.pdb'
            convert_cif_to_pdb(structure1, structure1_pdb)
            structure1 = structure1_pdb  # Update the structure1 path to the converted PDB
        elif ext1 == 'pdb' and ext2 == 'cif':
            #print(f"File formats are different. Converting {structure2} from CIF to PDB.")
            structure2_pdb = os.path.splitext(structure2)[0] + '.pdb'
            convert_cif_to_pdb(structure2, structure2_pdb)
            structure2 = structure2_pdb  # Update the structure2 path to the converted PDB

    unique_name1 = f"structure1_{uuid.uuid4().hex[:6]}"
    unique_name2 = f"structure2_{uuid.uuid4().hex[:6]}"
    
    # Load the structures
    pymol.cmd.load(structure1, unique_name1)
    pymol.cmd.load(structure2, unique_name2)

    # Superimpose the structures
    rmsd_value = pymol.cmd.super(unique_name1, unique_name2)

    if graph:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(current_dir, "aligned_structures.png")

        pymol.cmd.show("cartoon", unique_name1)
        pymol.cmd.show("cartoon", unique_name2)
        pymol.cmd.color("red", unique_name1)
        pymol.cmd.color("blue", unique_name2)
        pymol.cmd.zoom(unique_name1)
        pymol.cmd.zoom(unique_name2)

        pymol.cmd.png(output_path, width=800, height=600, dpi=300)
        #print(f"Image saved as: {output_path}")

    pymol.cmd.delete("all")

    pymol.finish_launching(['pymol', '-c'])

    return rmsd_value[0]

def process_files(folder_path):
    """
    Main function that goes through all JSON files in the specified folder,
    calling appropriate processing functions for each file type.
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            csv_filename = os.path.join(folder_path, filename)
            break
    df = pd.read_csv(csv_filename)

    # Iterate over files in the folder
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # Check if the file matches the pattern for fold_{unique_id}_full_data_0.json
            if filename.endswith("_full_data_0.json") and filename.startswith("fold_"):
                # Extract the unique identifier
                match = re.search(r"fold_([\d_]+)_full_data_0\.json", filename)
                if match:
                    unique_id = match.group(1)
                    file_path = os.path.join(root, filename)
                    unique_id, atom_plddts_mean_str, pae_mean_str = process_full_data_file_alphafold(file_path, unique_id)

                    # Look for the corresponding fold_{unique_id}_summary_confidences_0.json file
                    summary_filename = f"fold_{unique_id}_summary_confidences_0.json"
                    summary_file_path = os.path.join(root, summary_filename)
                    ptm_score_str = process_summary_confidences_file(summary_file_path)

                    adjusted_unique_id = unique_id[:10].replace("_", "-") + unique_id[10:]

                    # RMSD calculation
                    structure1 = os.path.join(root, f"fold_{unique_id}_model_0.cif")
                    
                    structure2 = os.path.join(root, f"{adjusted_unique_id}_target.pdb")

                    rmsd_value = pymol_rmsd(structure1, structure2, graph=False)
                
                    print(f"File ID: {unique_id}")
                    print("Alphafold 3 Metrics")
                    print(f"Mean of pLDDT Score: {atom_plddts_mean_str}")
                    print(f"Mean of PAE Score: {pae_mean_str}")
                    print(f"PTM Score: {ptm_score_str}")
                    print(f"RMSD Value: {rmsd_value:.4f} Å\n")

                    row_index = df[df['Target'] == unique_id].index
                    if not row_index.empty:
                        row = row_index[0]
                        df.loc[row, 'pLDDT_Fold'] = atom_plddts_mean_str
                        df.loc[row, 'PAE_Fold'] = pae_mean_str
                        df.loc[row, 'pTM_Fold'] = ptm_score_str
                        df.loc[row, 'RMSD_Fold'] = f"{rmsd_value:.4f}"

            # Check if the file matches the pattern for protenix_{unique_id}_full_data.json
            elif filename.endswith("_full_data_sample_0.json") and filename.startswith("Photenix_"):
                # Extract the unique identifier
                match = re.search(r"Photenix_([\d_]+)_full_data_sample_0\.json", filename)
                if match:
                    unique_id = match.group(1)
                    file_path = os.path.join(root, filename)
                    unique_id, atom_plddts_mean_str, pae_mean_str = process_full_data_file_protenix(file_path, unique_id)

                    # Look for the corresponding protenix_{unique_id}_summary.json file
                    summary_filename = f"Photenix_{unique_id}_summary_confidence_sample_0.json"
                    summary_file_path = os.path.join(root, summary_filename)
                    ptm_score_str = process_summary_confidences_file(summary_file_path)

                    adjusted_unique_id = unique_id[:10].replace("_", "-") + unique_id[10:]

                    # RMSD calculation
                    structure1 = os.path.join(root, f"Photenix_{unique_id}_sample_0.cif")
                    structure2 = os.path.join(root, f"{adjusted_unique_id}_target.pdb")

                    rmsd_value = pymol_rmsd(structure1, structure2, graph=False)

                    print(f"File ID: {unique_id}")
                    print("Protenix Metrics")
                    print(f"Mean of pLDDT Score: {atom_plddts_mean_str}")
                    print(f"Mean of PAE Score: {pae_mean_str}")
                    print(f"PTM Score: {ptm_score_str}")
                    print(f"RMSD Value: {rmsd_value:.4f} Å\n")

                    row_index = df[df['Target'] == unique_id].index
                    if not row_index.empty:
                        row = row_index[0]
                        df.loc[row, 'pLDDT_Protenix'] = float(atom_plddts_mean_str.replace(',', '.'))
                        df.loc[row, 'PAE_Protenix'] = float(pae_mean_str.replace(',', '.'))
                        df.loc[row, 'pTM_Protenix'] = float(ptm_score_str.replace(',', '.'))
                        df.loc[row, 'RMSD_Protenix'] = f"{rmsd_value:.4f}"

            if filename.endswith("_0.npy") and filename.startswith("Chai_"):
                unique_id = re.search(r"Chai_([\d_]+)_rank_0\.npy", filename).group(1)

                if unique_id == "2024_07_06_00000149":
                    new_unique_id = f"{unique_id}_2"
                else:
                    new_unique_id = f"{unique_id}_1"

                file_path = os.path.join(root, filename)
                pae_mean_str = process_pae_npy(file_path)

                json_file_path = os.path.join(root, f"Chai_{unique_id}_rank_0.json")

                ptm_str = process_chai_json(json_file_path)

                adjusted_unique_id = new_unique_id[:10].replace("_", "-") + new_unique_id[10:]

                # RMSD calculation
                structure1 = os.path.join(root, f"Chai_{unique_id}_sample_0.cif")
                structure2 = os.path.join(root, f"{adjusted_unique_id}_target.pdb")

                rmsd_value = pymol_rmsd(structure1, structure2, graph=False)

                print(f"File ID: {unique_id}")
                print("Chai Metrics")
                print(f"Mean PAE Score: {pae_mean_str}")
                print(f"Aggregate Score: {ptm_str}")
                print(f"RMSD Value: {rmsd_value:.4f} Å\n")

                row_index = df[df['Target'] == new_unique_id].index
                if not row_index.empty:
                    row = row_index[0]
                    df.loc[row, 'PAE_Chai'] = pae_mean_str
                    df.loc[row, 'pTM_Chai'] = ptm_str
                    df.loc[row, 'RMSD_Chai'] = f"{rmsd_value:.4f}"
        
    df.to_csv(csv_filename, index=False)
    
if __name__ == "__main__":
    # Path to the CSV file
    file_path = '../data'
    process_files(file_path)