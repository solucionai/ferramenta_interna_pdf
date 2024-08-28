from flask import Flask, render_template, request, redirect, url_for
from PyPDF2 import PdfMerger
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Certifique-se de que a pasta de upload existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Página principal de upload
@app.route('/')
def upload_page():
    return render_template('index.html')

# Rota para processar o upload
@app.route('/upload', methods=['POST'])
def upload_files():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        image_pdfs = []
        pdf_files = []

        # Separando imagens de PDFs
        for file in uploaded_files:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Se o arquivo for uma imagem, converte em PDF
            if file.filename.lower().endswith(('png', 'jpg', 'jpeg')):
                img = Image.open(filepath)
                img = img.convert('RGB')
                pdf_image_path = filepath.replace(file.filename.split('.')[-1], 'pdf')
                img.save(pdf_image_path)
                image_pdfs.append(pdf_image_path)
            elif file.filename.lower().endswith('pdf'):
                pdf_files.append(filepath)

        # Mescla os PDFs
        output_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'final_output.pdf')
        merge_pdfs(image_pdfs, pdf_files, output_filename)
        
        # Redireciona para o download
        return redirect(url_for('download_file', filename='final_output.pdf'))

# Função para mesclar PDFs
def merge_pdfs(image_pdfs, pdf_files, output_filename):
    merger = PdfMerger()
    
    # Adiciona PDFs de imagens convertidas
    for pdf in image_pdfs:
        merger.append(pdf)
    
    # Adiciona os PDFs enviados
    for pdf in pdf_files:
        merger.append(pdf)
    
    # Salva o arquivo final
    merger.write(output_filename)
    merger.close()

# Rota para baixar o PDF final
@app.route('/download/<filename>')
def download_file(filename):
    return redirect(f'/uploads/{filename}')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
