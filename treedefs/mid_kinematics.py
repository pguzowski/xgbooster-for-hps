def getit_df(df):
    
    df['sum_nhits_1'] = df.loc[:, ['nhits1_p0','nhits1_p1','nhits1_p2']].sum(axis=1)
    df['sum_nhits_2'] = df.loc[:, ['nhits2_p0','nhits2_p1','nhits2_p2']].sum(axis=1)
    df['sum_nhits'] = df.loc[:, ['sum_nhits_1','sum_nhits_2']].sum(axis=1)
    

    return df

def getit(tf):
    df = tf.pandas.df(lambda branch:
            branch.name[:4] == b'type' or branch.name[:8] == b'startend' or (branch.name[:5] == b'nhits' and branch.name[5:6] in [b'1',b'2']) or branch.name[:2] == b'th' or branch.name[:3] == b'phi' or branch.name == b'opang' or branch.name == b'transverse'
            # mid:
            or branch.name[:5] == b'slice' or branch.name[:6] == b'trkshw' or branch.name[:3] == b'len' or branch.name == b'nhits_slice'
            )
    return getit_df(df)


featmap_vars = {
        'int':[ 'type1', 'type2', 'startend1','startend2','slice_ntrk', 'slice_nshw', 'nhits1_p0', 'nhits2_p0', 'nhits1_p1', 'nhits2_p1', 'nhits1_p2', 'nhits2_p2', 'nhits_other_pfps', 'nhits_beg1_p0', 'nhits_beg1_p1', 'nhits_beg1_p2', 'nhits_beg2_p0', 'nhits_beg2_p1', 'nhits_beg2_p2', 'nhits_slice', 'sum_nhits_1', 'sum_nhits_2', 'sum_nhits' ],
        'q':['vtx_x', 'vtx_y', 'vtx_z', 'dca', 'opang', 'th1', 'th2', 'phi1', 'phi2', 'b2b', 'transverse', 'next_dca', 'next_len', 'next_nhits', 'next_score', 'len1', 'len2', 'trkshw_score1', 'trkshw_score2', 'slice_nuscore', 'dca_hits_p0', 'dca_hits_p1', 'dca_hits_p2', 'dca_unassoc_vtx_p0', 'dca_unassoc_vtx_p1', 'dca_unassoc_vtx_p2', 'dca_othpfp_vtx_p0', 'dca_othpfp_vtx_p1', 'dca_othpfp_vtx_p2', 'flshtime_slice', 'mean_start_hitamp_asym_p0', 'mean_start_hitamp_asym_p1', 'mean_start_hitamp_asym_p2', 'slice_min_tick', 'slice_max_tick',  'tree_trkfit1_chi2_p0', 'tree_trkfit1_chi2_p1', 'tree_trkfit1_chi2_p2', 'tree_trkfit2_chi2_p0', 'tree_trkfit2_chi2_p1', 'tree_trkfit2_chi2_p2', 'tree_next_vtx_x_min', 'tree_next_vtx_x_neg', 'tree_next_vtx_x_pos', 'tree_next_vtx_x_max', 'tree_next_vtx_y_min', 'tree_next_vtx_y_neg', 'tree_next_vtx_y_pos', 'tree_next_vtx_y_max', 'tree_next_vtx_z_min', 'tree_next_vtx_z_neg', 'tree_next_vtx_z_pos', 'tree_next_vtx_z_max', 'tree_cand_min_x', 'tree_cand_max_x', 'tree_slice_min_x', 'tree_slice_max_x', 'tree_cand_min_y', 'tree_cand_max_y', 'tree_slice_min_y', 'tree_slice_max_y', 'tree_cand_min_z', 'tree_cand_max_z', 'tree_slice_min_z', 'tree_slice_max_z' ],
        'i':['slice_is_neutrino', 'b2b_p0', 'b2b_p1', 'b2b_p2'],
        }

featmap = 'featmaps/featmap_midkin.txt'
