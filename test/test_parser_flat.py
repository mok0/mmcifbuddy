import pytest
from pathlib import Path
from mmcifbuddy import ParserFlat

thedata = {}

@pytest.fixture(autouse=True, scope="session")
def get_dict():
    myparser = ParserFlat(verbose=False)
    cwd = Path(__file__).parent
    fnam = Path(cwd, "4af1.cif")
    myparser.fopen(fnam)
    _ = myparser.parse()
    thedata.update(myparser.get_dict())
    myparser.fclose()
    yield thedata

## Tests below

def test_entry_id():
    assert "4AF1" == thedata['_entry.id']

def test_audit_version():
    assert 5.308 == thedata['_audit_conform.dict_version']

def test_database_code():
    assert "D_1290049908" == thedata['_database_2.database_code'][2]

def test_audit_authors():
    assert "Karlsen, J.L." == thedata['_audit_author.name'][0]
    assert "Kjeldgaard, M." == thedata['_audit_author.name'][1]

def test_citation_title():
    title = 'Archeal Release Factor Arf1 Contains a Metal Binding Domain'
    assert title == thedata['_citation.title']

def test_citation_authors():
    assert "Karlsen, J.L." == thedata['_citation_author.name'][0]
    assert "Kjeldgaard, M." == thedata['_citation_author.name'][1]

def test_cell():
    assert "4AF1" == thedata['_cell.entry_id']
    assert 131.02 == thedata['_cell.length_a']
    assert 31.99 == thedata['_cell.length_b']
    assert 111.15 == thedata['_cell.length_c']
    assert 90.0 == thedata['_cell.angle_alpha']
    assert 113.47 == thedata['_cell.angle_beta']
    assert 90.0 == thedata['_cell.angle_gamma']
    assert 4 == thedata['_cell.Z_PDB']

def test_symmetry():
    assert "4AF1" == thedata['_symmetry.entry_id']
    assert "C 1 2 1" == thedata['_symmetry.space_group_name_H-M']
    assert 5 == thedata['_symmetry.Int_Tables_number']

def test_entity():
    assert 1 == thedata['_entity.id'][0]
    assert 2 == thedata['_entity.id'][1]
    assert 3 == thedata['_entity.id'][2]
    assert 46692.48 == thedata['_entity.formula_weight'][0]
    assert 65.409 == thedata['_entity.formula_weight'][1]
    assert 18.015 == thedata['_entity.formula_weight'][2]
    assert "ZINC ION" == thedata['_entity.pdbx_description'][1]
    assert 181 == thedata['_entity.pdbx_number_of_molecules'][2]
    assert "3.6.5.3" == thedata['_entity.pdbx_ec'][0]

def test_entity_name_com():
    name = "TRANSLATION TERMINATION FACTOR ARF1, RELEASE FACTOR 1"
    assert 1 == thedata['_entity_name_com.entity_id']
    assert name == thedata['_entity_name_com.name']

def test_entity_poly():
    assert "polypeptide(L)" == thedata['_entity_poly.type']
    assert 6 == len(thedata['_entity_poly.pdbx_seq_one_letter_code'])
    assert 6 == len(thedata['_entity_poly.pdbx_seq_one_letter_code_can'])
    assert "A" == thedata['_entity_poly.pdbx_strand_id']
    seq = ''.join(thedata['_entity_poly.pdbx_seq_one_letter_code'])
    assert 416 == len(seq)

def test_entity_poly_seq():
    assert 416 == len(thedata['_entity_poly_seq.mon_id'])
    assert "PRO" == thedata['_entity_poly_seq.mon_id'][7]

def test_entity_src_gen():
    assert "HALOBACTERIUM SALINARUM" == thedata['_entity_src_gen.pdbx_gene_src_scientific_name']
    assert "ESCHERICHIA COLI" == thedata['_entity_src_gen.pdbx_host_org_scientific_name']
    assert "PET19B" == thedata['_entity_src_gen.pdbx_host_org_vector']

def test_struct_ref():
    assert "RF1_HALSA" == thedata['_struct_ref.db_code']
    assert "Q9HNF0" == thedata['_struct_ref.pdbx_db_accession']

def test_struct_ref_seq():
    assert "4AF1" == thedata['_struct_ref_seq.pdbx_PDB_id_code']
    assert 416 == thedata['_struct_ref_seq.seq_align_end']
    assert 416 == thedata['_struct_ref_seq.pdbx_auth_seq_align_end']
    assert "Q9HNF0" == thedata['_struct_ref_seq.pdbx_db_accession']

def test_chem_comp():
    assert 22 == len(thedata['_chem_comp.id'])
    assert 'ZINC ION' == thedata['_chem_comp.name'][-1]
    assert "C4 H7 N O4" == thedata['_chem_comp.formula'][3]
    assert 18.015 == thedata['_chem_comp.formula_weight'][9]

def test_exptl():
    assert "4AF1" == thedata['_exptl.entry_id']
    assert "X-RAY DIFFRACTION" == thedata['_exptl.method']
    assert 1 == thedata['_exptl.crystals_number']

def test_exptl_crystal():
    assert 1 == thedata['_exptl_crystal.id']
    assert 2.27 == thedata['_exptl_crystal.density_Matthews']
    assert 45.8 == thedata['_exptl_crystal.density_percent_sol']

def test_exptl_crystal_grow():
    assert "VAPOR DIFFUSION, SITTING DROP" == thedata['_exptl_crystal_grow.method']
    assert 8 == thedata['_exptl_crystal_grow.pH']
    assert 130 == len(thedata['_exptl_crystal_grow.pdbx_details'])
    assert str == type(thedata['_exptl_crystal_grow.pdbx_details'])

def test_diffrn():
    assert 1 == thedata['_diffrn_detector.diffrn_id']
    assert "CCD" == thedata['_diffrn_detector.detector']
    assert "ADSC QUANTUM 210" == thedata['_diffrn_detector.type']
    assert "2004-06-30" == thedata['_diffrn_detector.pdbx_collection_date']

def test_diffrn_radiation():
    assert "SINGLE WAVELENGTH" == thedata['_diffrn_radiation.pdbx_diffrn_protocol']
    assert "x-ray" == thedata['_diffrn_radiation.pdbx_scattering_type']
    assert 0.9756 == thedata['_diffrn_radiation_wavelength.wavelength']

def test_diffrn_source():
    assert "SYNCHROTRON" == thedata['_diffrn_source.source']
    assert "ESRF BEAMLINE ID29" == thedata['_diffrn_source.type']
    assert "ESRF" == thedata['_diffrn_source.pdbx_synchrotron_site']

def test_reflns():
    assert 1 == thedata['_reflns.pdbx_diffrn_id']
    assert "4AF1" == thedata['_reflns.entry_id']
    assert 64.16 == thedata['_reflns.d_resolution_low']
    assert 2.0 == thedata['_reflns.d_resolution_high']
    assert 29222 == thedata['_reflns.number_obs']
    assert 94.7 == thedata['_reflns.percent_possible_obs']
    assert 0.09 == thedata['_reflns.pdbx_Rmerge_I_obs']
    assert 13.40 == thedata['_reflns.pdbx_netI_over_sigmaI']
    assert 29.24 == thedata['_reflns.B_iso_Wilson_estimate']

def test_reflns_shell():
    assert 1 == thedata['_reflns_shell.pdbx_diffrn_id']
    assert 2.0 == thedata['_reflns_shell.d_res_high']
    assert 2.05 == thedata['_reflns_shell.d_res_low']
    assert 48.0 == thedata['_reflns_shell.percent_possible_all']
    assert 1.23 == thedata['_reflns_shell.Rmerge_I_obs']
    assert 2.30 == thedata['_reflns_shell.meanI_over_sigI_obs']
    assert 3.5 == thedata['_reflns_shell.pdbx_redundancy']

def test_refine():

    assert "4AF1" == thedata['_refine.entry_id']
    assert 29073 == thedata['_refine.ls_number_reflns_obs']
    assert 94.7 == thedata['_refine.ls_percent_reflns_obs']
    assert 0.255 == thedata['_refine.ls_R_factor_obs']
    assert 0.2537 == thedata['_refine.ls_R_factor_R_work']
    assert 0.2788 == thedata['_refine.ls_R_factor_R_free']
    assert 1385 == thedata['_refine.ls_number_reflns_R_free']
    assert -2.2384 == thedata['_refine.aniso_B[3][3]']
    assert "FLAT BULK SOLVENT MODEL" == thedata['_refine.solvent_model_details']
    assert "PDB ENTRY 1DT9" == thedata['_refine.pdbx_starting_model']
    assert 31.52 == thedata['_refine.pdbx_overall_phase_error']

def test_refine_ls_restr():
    assert 5 == len(thedata['_refine_ls_restr.type'])
    assert 13.559 == thedata['_refine_ls_restr.dev_ideal'][2]
    assert 4439 == thedata['_refine_ls_restr.number'][1]

def test_refine_ls_shell():
    assert 10 == len(thedata['_refine_ls_shell.pdbx_refine_id'])
    assert 1485 == thedata['_refine_ls_shell.number_reflns_R_work'][0]

def test_struct():
    assert "Archeal Release Factor aRF1" == thedata['_struct.title']
    assert "4AF1" == thedata['_struct_keywords.entry_id']

def test_struct_conf():
    assert 14 == len(thedata['_struct_conf.id'])

def test_struct_conn():
    assert 5 == len(thedata['_struct_conn.id'])

def test_atom_site():
    assert 3405 == len(thedata['_atom_site.id'])
    assert "CG2" == thedata['_atom_site.label_atom_id'][6]
    assert -20.014 == thedata['_atom_site.Cartn_y'][8]
    assert 34.03 == thedata['_atom_site.B_iso_or_equiv'][3404]

def test_atom_site_anisotrop():
    assert 3224 == len(thedata['_atom_site_anisotrop.id'])

def test_pdbx_poly_seq_scheme():
    assert 416 == len(thedata['_pdbx_poly_seq_scheme.asym_id'])

def test_pdbx_nonpoly_scheme():
    assert 182 == len(thedata['_pdbx_nonpoly_scheme.asym_id'])

def test_pdbx_entity_nonpoly():
    assert 2 == len(thedata['_pdbx_entity_nonpoly.entity_id'])
