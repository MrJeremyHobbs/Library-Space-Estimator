#!/usr/bin/python3
import csv
import os

### Notes ###
### -- can only count if an item record is present in system

# Clean-up
#os.system('del output.txt')

### LIST BINS TO PLACE PHYSICAL ITEMS INTO FOR CLASSIFICATION #################
cd = []
dvd = []
childrens_books = []
fiction_economics_books = []
history_general_literature = []
reference = []
technical_scientific = []
medical = []
law_public_documents = []
bound_periodicals = []
scores = []
misc = []

### MAIN ######################################################################
def main():
    with open("historical.csv", newline='\n', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        # Loop through CSV holdings and place in list
        for row in reader:
            barcode = row[0]
            call_number = row[1]
            title = row[2]
            material_type = row[3]
            location = row[4]
            type_of_media = ""
            
            # normalize values
            call_number = call_number.replace("OVR ", "")
            call_number = call_number.upper()
            
            # skip header
            if material_type == "Material Type":
                continue
            
            type_of_media = classify(location=location, material_type=material_type, barcode=barcode, call_number=call_number)
        
        # totals
        total_volumes = "{:,}".format(grand_totals_vols())
        total_lf = "{:,}".format(grand_total_lf())
        
        print(f"""
TYPE OF MEDIA               INVENTORY COUNT
-------------               ---------------
cd                          {len(cd)}
dvd                         {len(dvd)}
childrens_books             {len(childrens_books)}
fiction_economics_books     {len(fiction_economics_books)}
history_general_literature  {len(history_general_literature)}
reference                   {len(reference)}
technical_scientific        {len(technical_scientific)}
medical                     {len(medical)}
law_public_documents        {len(law_public_documents)}
bound_periodicals           {len(bound_periodicals)}
scores                      {len(scores)}
misc                        {len(misc)}

TOTALS
------
total_volumes               {total_volumes}
total_linear_feet           {total_lf}
        """)
         
     
### FUNCTIONS #################################################################
def classify(location="", material_type="", barcode="", call_number=""):
        # CDs
        cd_mat_types = ["Computer Disk", "Compact Disc", "CD-ROM"]
        if material_type in cd_mat_types:
            cd.append(barcode)
        
        # DVDs
        if location == "DVDs - 2nd Floor":
            dvd.append(barcode)
            return "dvds"
            
        # Law and public documents
        doc_locations = ["K",
                         "AGX Documents - 2nd Floor", 
                         "California Documents - 2nd Floor", 
                         "California Documents - Ask at Research Help Desk - 2nd Floor", 
                         "Diablo Canyon Collection - 4th Floor",
                         "Federal Documents - Ask at Research Help Desk - 2nd Floor",
                         "Local Documents - 2nd Floor",
                         "Local Documents - Ask at Research Help Desk - 2nd Floor",
                         "Soil Surveys - 2nd Floor"]
                         
        if location in doc_locations:
            law_public_documents.append(barcode)
            return "law_public_documents"
            
        if call_number[:1] in doc_locations:
            law_public_documents.append(barcode)
            return "law_public_documents"
            
        # Bound periodicals
        bound_per_mat_types = ["Issue", "Bound Issue"]
        if material_type in bound_per_mat_types:
            bound_periodicals.append(barcode)
            return "bound_periodicals"
            
        # Scores
        if material_type == "Music Score":
            scores.append(barcode)
            return "scores"
        
        # Children's books
        if location == "Teachers' Resource Collection - 3rd Floor" \
          or location == "Teachers' Resource Collection - Spanish - 3rd Floor":
            childrens_books.append(barcode)
            return "childrens_books"
            
        # Reference
        ref_locations = ["Research Help - 2nd Floor"]
        if location in ref_locations:
            reference.append(barcode)
            return "reference"
        
        # Fiction and economic books
        if location == "Good Reads - 2nd Floor":
            fiction_economics_books.append(barcode)
            return "fiction_economics_books"
            
        fict_econ_locations = ["H", "P"]
        if call_number[:1] in fict_econ_locations:
            fiction_economics_books.append(barcode)
            return "fiction_economics_books"
        
        # History and general literature
        gen_lit_locations = ["A", "B", "C", "D", "E", "F", "H", "J", "L", "M", 
                             "N", "P", "Z"]
        if call_number[:1] in gen_lit_locations:
            history_general_literature.append(barcode)
            return "history_general_literature"
        
        # Technical and scientific
        tech_locations = ["G", "Q", "S", "T", "U", "V"]
        if call_number[:1] in tech_locations:
            technical_scientific.append(barcode)
            return "technical_scientific"
        
        # Medical
        if call_number[:1] == "R":
            medical.append(barcode)
            return "medical"
            
        misc.append(barcode)
        return "misc"

def grand_totals_vols():
    totals = [len(cd),
    len(dvd),
    len(childrens_books),
    len(fiction_economics_books),
    len(history_general_literature),
    len(reference),
    len(technical_scientific),
    len(medical),
    len(law_public_documents),
    len(bound_periodicals),
    len(scores),
    len(misc),
    ]
    
    grand_total = sum(totals)
        
    return grand_total
        
def grand_total_lf():
    cd_lf = len(cd) / 12   
    dvd_lf = len(dvd) / 12
    childrens_books_lf = len(childrens_books) / 12
    fiction_economics_books_lf = len(fiction_economics_books) / 12
    history_general_literature_lf = len(history_general_literature) / 12
    reference_lf = len(reference) / 12
    technical_scientific_lf = len(technical_scientific) / 12
    medical_lf = len(medical) / 12
    law_public_documents_lf = len(law_public_documents) / 12
    bound_periodicals_lf = len(bound_periodicals) / 12
    scores_lf = len(bound_periodicals) / 12
    misc_lf =  len(bound_periodicals) / 12

    totals = [cd_lf,
    dvd_lf,
    childrens_books_lf,
    fiction_economics_books_lf,
    history_general_literature_lf,
    reference_lf,
    technical_scientific_lf,
    medical_lf,
    law_public_documents_lf,
    bound_periodicals_lf,
    scores_lf,
    misc_lf,
    ]
    
    print(reference_lf)

    grand_total = 0
    for total in totals:
        grand_total += total
        
    return grand_total
    

### TOP-LEVEL #################################################################        
if __name__ == "__main__":
    main()