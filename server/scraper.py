import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import sys

def scrape(character_name,):
    # Scrape Wikipedia
    url = "https://en.wikipedia.org/wiki/"+character_name
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find(id='mw-content-text').get_text()

    # Chunk Text
    def chunk_text(text, chunk_size=300):
        words = text.split()
        return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    chunks = chunk_text(content)

    # Create a PDF class inheriting from FPDF
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10,f'{character_name} Wikipedia Content', 0, 1, 'C')
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
        def chapter_title(self, chapter_title):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, chapter_title, 0, 1, 'L')
            self.ln(10)
        

        def chapter_body(self, body):
            self.set_font('Arial', '', 12)
            if sys.version_info >= (3, 0):
                body = body.encode('latin-1', 'replace').decode('latin-1')
            self.multi_cell(0, 10, body)
            self.ln()



    pdf = PDF()
    pdf.add_page()

    # Add content to PDF
    pdf.set_title(f'{character_name} Wikipedia Content')

    for i, chunk in enumerate(chunks):
        pdf.chapter_title(f'Section {i+1}')
        pdf.chapter_body(chunk)

    # Save PDF
    pdf_output_path = f'{character_name}_Wikipedia_Content.pdf'
    pdf.output(pdf_output_path)

    print(f'PDF saved to {pdf_output_path}')


character_list=[
    'Luke_Skywalker',
    'Admiral_Ackbar',
    'The_Armorer',
    'Wedge_Antilles',
    'Doctor_Aphra',
    'Cad_Bane',
    'Darth_Bane',
    'Tobias_Beckett',
    'Jar_Jar_Binks',
    'Ezra_Bridger',
    'Lando_Calrissian',
    'Chewbacca',
    'The_Client_(Star_Wars)',
    'Poe_Dameron',
    'The_Mandalorian_(character)',
    'Count_Dooku',
    'Kanan_Jarrus',
    'Cara_Dune',
    'Jyn_Erso',
    'Boba_Fett',
    'Jango_Fett',
    'Finn_(Star_Wars)',
    'Bib_Fortuna',
    'Saw_Gerrera',
    'Moff_Gideon',
    'Han_shot_first',
    'General_Grievous',
    'Grogu',
    'Vice-Admiral_Holdo',
    'General_Hux',
    'Jabba_the_Hutt',
    'Qui-Gon_Jinn',
    'Maz_Kanata',
    'Greef_Karga',
    'Obi-Wan_Kenobi',
    'Cal_Kestis',
    'Orson_Krennic',
    'Black_Krrsantan',
    'Bo-Katan_Kryze',
    'Darth_Maul',
    'Migs_Mayfeld',
    'Mon_Mothma',
    'Princess_Leia',
    'Palpatine',
    'Captain_Phasma',
    'Admiral_Piett',
    'Qui-Gon_Jinn',
    'Ren_(Star_Wars)',
    'Captain_Rex',
    'Rey_(Star_Wars)',
    'Fennec_Shand',
    'Darth_Vader',
    'Supreme_Leader_Snoke',
    'Kylo_Ren',
    'Han_Solo',
    'Hera_Syndulla',
    'Ahsoka_Tano',
    'Grand_Moff_Tarkin',
    'Grand_Admiral_Thrawn',
    'Cobb_Vanth',
    'Asajj_Ventress',
    'Iden_Versio',
    'Paz_Vizsla',
    'Wicket_W._Warrick',
    'Watto',
    'Mace_Windu',
    'Sabine_Wren',
    'Yoda',
    'List_of_Star_Wars_characters'
    ]

# for character_name in character_list:
#     scrape(character_name)
    # print(f'{character_name} is a character\n')

scrape('List_of_Star_Wars_characters')