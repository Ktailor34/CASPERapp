# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/home/trinhlab/Desktop/CASPERapp'],
             binaries=[
				('CasperSeqFinderLinux', '.')
			 ],
             datas=[
				('OffTargetFolder', 'OffTargetFolder'),
				('CASPERinfo', '.'),
				('Casperimg.icns', '.'),
				('Codonimg.icns', '.'),
				('myicon.ico', '.'),
				('mainart.jpg', '.'),
				('cas9image.png', '.'),
				('Annotation Details.ui', '.'),
				('CASPER_main.ui', '.'),
				('closingWindow.ui', '.'),
				('co_targeting.ui', '.'),
				('cspr_chromesome_selection.ui', '.'),
				('export_to_csv_window.ui', '.'),
				('geneViewerSettings.ui', '.'),
				('library_prompt.ui', '.'),
				('multitargetingwindow.ui', '.'),
				('NCBI_File_Search.ui', '.'),
				('NewGenome.ui', '.'),
				('OffTargetAnalysis.ui', '.'),
				('OffTargetProgress.ui', '.'),
				('populationanalysis.ui', '.'),
				('resultsWindow.ui', '.'),
				('startupCASPER.ui', '.'),
				('pop_analysis_fna_combiner.ui', '.'),
				('name_form.ui', '.'),
				('name_form2.ui', '.')

			 ],
             hiddenimports=[
				'repeats_vs_seeds_line', 
				'seeds_vs_repeats_bar', 
				'repeats_vs_chromo',
				'pop_analysis_3dgraph',
				'pop_analysis_repeats_graph',
				'pop_analysis_venn_diagram'
			],
             hookspath=[],
             runtime_hooks=[],
             excludes=[
				 'cryptography',
				 'Crypto'
			 ],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='CASPERapp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='CASPERapp')
