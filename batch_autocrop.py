import os
import glob 

os.chdir(r'E:\~entity\Quicksilver Designs\~Projects\DVDCatalog\src\python\page_generator\tests\dvd_covers')

filenames = [file for file in glob.glob('*.jpg')]

for filename in filenames:
	filename = os.getcwd()+ '\\' + filename
	image = pdb.gimp_file_load(filename, filename)
	drawable = pdb.gimp_image_get_active_layer(image)  
	
	pdb.plug_in_autocrop(image, drawable)
	pdb.gimp_file_save(image, drawable, filename, filename)
	pdb.gimp_image_delete(image)
   
   