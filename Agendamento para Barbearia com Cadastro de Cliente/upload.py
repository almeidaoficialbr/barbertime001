import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from PIL import Image
import mimetypes
from src.models import db, TenantConfig
from src.middleware.tenant import get_current_tenant

upload_bp = Blueprint('upload', __name__)

# Configurações de upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
UPLOAD_FOLDER = 'uploads'
LOGO_SIZES = [(200, 200), (100, 100), (50, 50)]  # Diferentes tamanhos para logos

def allowed_file(filename):
    """Verificar se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_upload_folder():
    """Criar pasta de uploads se não existir"""
    upload_path = os.path.join(current_app.root_path, '..', 'static', UPLOAD_FOLDER)
    os.makedirs(upload_path, exist_ok=True)
    return upload_path

def resize_image(image_path, sizes):
    """Redimensionar imagem para diferentes tamanhos"""
    resized_paths = []
    
    try:
        with Image.open(image_path) as img:
            # Converter para RGB se necessário
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            base_name = os.path.splitext(image_path)[0]
            extension = os.path.splitext(image_path)[1]
            
            for width, height in sizes:
                # Redimensionar mantendo proporção
                img_resized = img.copy()
                img_resized.thumbnail((width, height), Image.Resampling.LANCZOS)
                
                # Criar nova imagem com fundo branco se necessário
                if img_resized.size != (width, height):
                    new_img = Image.new('RGB', (width, height), (255, 255, 255))
                    paste_x = (width - img_resized.width) // 2
                    paste_y = (height - img_resized.height) // 2
                    new_img.paste(img_resized, (paste_x, paste_y))
                    img_resized = new_img
                
                # Salvar imagem redimensionada
                resized_path = f"{base_name}_{width}x{height}{extension}"
                img_resized.save(resized_path, quality=85, optimize=True)
                resized_paths.append(resized_path)
    
    except Exception as e:
        print(f"Erro ao redimensionar imagem: {e}")
        return []
    
    return resized_paths

@upload_bp.route('/logo', methods=['POST'])
@jwt_required()
def upload_logo():
    """Upload de logo da barbearia"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        # Verificar se arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Verificar extensão do arquivo
        if not allowed_file(file.filename):
            return jsonify({'error': 'Tipo de arquivo não permitido'}), 400
        
        # Verificar tamanho do arquivo
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': 'Arquivo muito grande. Máximo 5MB'}), 400
        
        # Criar pasta de uploads
        upload_path = create_upload_folder()
        tenant_folder = os.path.join(upload_path, f'tenant_{tenant.id}')
        os.makedirs(tenant_folder, exist_ok=True)
        
        # Gerar nome único para o arquivo
        file_extension = secure_filename(file.filename).rsplit('.', 1)[1].lower()
        unique_filename = f"logo_{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join(tenant_folder, unique_filename)
        
        # Salvar arquivo original
        file.save(file_path)
        
        # Redimensionar para diferentes tamanhos (apenas para imagens não SVG)
        resized_paths = []
        if file_extension != 'svg':
            resized_paths = resize_image(file_path, LOGO_SIZES)
        
        # Gerar URLs públicas
        base_url = f"/static/{UPLOAD_FOLDER}/tenant_{tenant.id}/{unique_filename}"
        logo_urls = {
            'original': base_url
        }
        
        # Adicionar URLs das versões redimensionadas
        for i, (width, height) in enumerate(LOGO_SIZES):
            if i < len(resized_paths):
                resized_filename = os.path.basename(resized_paths[i])
                logo_urls[f'{width}x{height}'] = f"/static/{UPLOAD_FOLDER}/tenant_{tenant.id}/{resized_filename}"
        
        # Atualizar configuração do tenant
        config = TenantConfig.query.filter_by(tenant_id=tenant.id).first()
        if not config:
            config = TenantConfig(tenant_id=tenant.id)
            db.session.add(config)
        
        config.logo_url = logo_urls['original']
        db.session.commit()
        
        return jsonify({
            'message': 'Logo enviado com sucesso',
            'logo_urls': logo_urls,
            'file_info': {
                'filename': unique_filename,
                'size': file_size,
                'type': mimetypes.guess_type(file_path)[0]
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao fazer upload: {str(e)}'}), 500

@upload_bp.route('/gallery', methods=['POST'])
@jwt_required()
def upload_gallery_image():
    """Upload de imagem para galeria da barbearia"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        # Verificar se arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Verificar extensão do arquivo
        if not allowed_file(file.filename):
            return jsonify({'error': 'Tipo de arquivo não permitido'}), 400
        
        # Verificar tamanho do arquivo
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': 'Arquivo muito grande. Máximo 5MB'}), 400
        
        # Criar pasta de uploads
        upload_path = create_upload_folder()
        tenant_folder = os.path.join(upload_path, f'tenant_{tenant.id}', 'gallery')
        os.makedirs(tenant_folder, exist_ok=True)
        
        # Gerar nome único para o arquivo
        file_extension = secure_filename(file.filename).rsplit('.', 1)[1].lower()
        unique_filename = f"gallery_{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join(tenant_folder, unique_filename)
        
        # Salvar arquivo original
        file.save(file_path)
        
        # Redimensionar para galeria (tamanhos específicos)
        gallery_sizes = [(800, 600), (400, 300), (200, 150)]  # Grande, médio, thumbnail
        resized_paths = resize_image(file_path, gallery_sizes)
        
        # Gerar URLs públicas
        base_url = f"/static/{UPLOAD_FOLDER}/tenant_{tenant.id}/gallery/{unique_filename}"
        image_urls = {
            'original': base_url
        }
        
        # Adicionar URLs das versões redimensionadas
        size_names = ['large', 'medium', 'thumbnail']
        for i, (width, height) in enumerate(gallery_sizes):
            if i < len(resized_paths):
                resized_filename = os.path.basename(resized_paths[i])
                image_urls[size_names[i]] = f"/static/{UPLOAD_FOLDER}/tenant_{tenant.id}/gallery/{resized_filename}"
        
        return jsonify({
            'message': 'Imagem enviada com sucesso',
            'image_urls': image_urls,
            'file_info': {
                'filename': unique_filename,
                'size': file_size,
                'type': mimetypes.guess_type(file_path)[0]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao fazer upload: {str(e)}'}), 500

@upload_bp.route('/files/<path:filename>', methods=['DELETE'])
@jwt_required()
def delete_file(filename):
    """Excluir arquivo enviado"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        # Construir caminho do arquivo
        upload_path = create_upload_folder()
        tenant_folder = os.path.join(upload_path, f'tenant_{tenant.id}')
        file_path = os.path.join(tenant_folder, secure_filename(filename))
        
        # Verificar se arquivo existe e pertence ao tenant
        if not os.path.exists(file_path):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        # Verificar se o caminho está dentro da pasta do tenant (segurança)
        if not os.path.commonpath([file_path, tenant_folder]) == tenant_folder:
            return jsonify({'error': 'Acesso negado'}), 403
        
        # Excluir arquivo
        os.remove(file_path)
        
        # Excluir versões redimensionadas se existirem
        base_name = os.path.splitext(file_path)[0]
        extension = os.path.splitext(file_path)[1]
        
        for width, height in LOGO_SIZES + [(800, 600), (400, 300), (200, 150)]:
            resized_path = f"{base_name}_{width}x{height}{extension}"
            if os.path.exists(resized_path):
                os.remove(resized_path)
        
        return jsonify({'message': 'Arquivo excluído com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao excluir arquivo: {str(e)}'}), 500

@upload_bp.route('/files', methods=['GET'])
@jwt_required()
def list_files():
    """Listar arquivos enviados pelo tenant"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        # Construir caminho da pasta do tenant
        upload_path = create_upload_folder()
        tenant_folder = os.path.join(upload_path, f'tenant_{tenant.id}')
        
        files = []
        
        if os.path.exists(tenant_folder):
            for root, dirs, filenames in os.walk(tenant_folder):
                for filename in filenames:
                    # Pular arquivos redimensionados (que contêm dimensões no nome)
                    if '_' in filename and 'x' in filename.split('_')[-1]:
                        continue
                    
                    file_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(file_path, tenant_folder)
                    
                    # Obter informações do arquivo
                    stat = os.stat(file_path)
                    file_info = {
                        'filename': filename,
                        'path': relative_path,
                        'size': stat.st_size,
                        'created_at': stat.st_ctime,
                        'type': mimetypes.guess_type(file_path)[0],
                        'url': f"/static/{UPLOAD_FOLDER}/tenant_{tenant.id}/{relative_path}"
                    }
                    
                    files.append(file_info)
        
        return jsonify({
            'files': files,
            'total': len(files)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao listar arquivos: {str(e)}'}), 500

