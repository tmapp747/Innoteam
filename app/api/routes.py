from flask import jsonify, request, current_app
from app.api import api_bp
from app.models.user import User, Website
from app import db, limiter
from app.utils.website_generator import ModernWebsiteCrew
from functools import wraps
from datetime import datetime

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({'error': 'API key is required'}), 401
            
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            return jsonify({'error': 'Invalid API key'}), 401
            
        return f(user, *args, **kwargs)
    return decorated_function

@api_bp.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded', 'description': str(e.description)}), 429

@api_bp.route('/websites', methods=['GET'])
@require_api_key
@limiter.limit("100 per day")
def list_websites(user):
    websites = Website.query.filter_by(user_id=user.id).all()
    return jsonify({
        'websites': [website.to_dict() for website in websites]
    })

@api_bp.route('/websites', methods=['POST'])
@require_api_key
@limiter.limit("10 per day")
def create_website(user):
    try:
        data = request.get_json()
        if not data or 'idea' not in data:
            return jsonify({'error': 'Website idea is required'}), 400

        # Create website record
        website = Website(
            name=data.get('name', f"Website-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"),
            description=data['idea'],
            user_id=user.id,
            status='generating'
        )
        db.session.add(website)
        db.session.commit()

        # Initialize website generator
        crew = ModernWebsiteCrew(
            idea=data['idea'],
            llm_type=data.get('llm_type'),
            api_key=user.api_key,
            website_id=website.id
        )

        # Generate website
        result = crew.run()

        # Update website record
        website.status = 'completed'
        website.configuration = {
            'llm_type': data.get('llm_type'),
            'generation_result': result,
            'conversation_log': crew.conversation_log
        }
        db.session.commit()

        return jsonify({
            'message': 'Website generated successfully',
            'website': website.to_dict(),
            'result': result
        })

    except Exception as e:
        if website:
            website.status = 'failed'
            website.configuration = {
                'error': str(e),
                'llm_type': data.get('llm_type')
            }
            db.session.commit()
        
        current_app.logger.error(f"API website generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/websites/<int:website_id>', methods=['GET'])
@require_api_key
@limiter.limit("1000 per day")
def get_website(user, website_id):
    website = Website.query.get_or_404(website_id)
    if website.user_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify(website.to_dict())

@api_bp.route('/websites/<int:website_id>', methods=['DELETE'])
@require_api_key
@limiter.limit("50 per day")
def delete_website(user, website_id):
    website = Website.query.get_or_404(website_id)
    if website.user_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    db.session.delete(website)
    db.session.commit()
    return jsonify({'message': 'Website deleted successfully'})

@api_bp.route('/websites/<int:website_id>/regenerate', methods=['POST'])
@require_api_key
@limiter.limit("5 per day")
def regenerate_website(user, website_id):
    website = Website.query.get_or_404(website_id)
    if website.user_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        # Update status
        website.status = 'regenerating'
        db.session.commit()

        # Initialize website generator
        crew = ModernWebsiteCrew(
            idea=website.description,
            llm_type=website.configuration.get('llm_type'),
            api_key=user.api_key,
            website_id=website.id
        )

        # Regenerate website
        result = crew.run()

        # Update website record
        website.status = 'completed'
        website.configuration.update({
            'regeneration_result': result,
            'regeneration_date': datetime.utcnow().isoformat(),
            'conversation_log': crew.conversation_log
        })
        db.session.commit()

        return jsonify({
            'message': 'Website regenerated successfully',
            'website': website.to_dict(),
            'result': result
        })

    except Exception as e:
        website.status = 'failed'
        website.configuration['error'] = str(e)
        db.session.commit()
        
        current_app.logger.error(f"API website regeneration error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/status', methods=['GET'])
@limiter.limit("100 per minute")
def api_status():
    return jsonify({
        'status': 'operational',
        'version': '1.0',
        'timestamp': datetime.utcnow().isoformat()
    })
