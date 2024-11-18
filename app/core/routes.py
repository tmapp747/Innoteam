from flask import render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from app.core import core_bp
from app.models.user import Website
from app import db, limiter, cache
from app.utils.website_generator import ModernWebsiteCrew
from datetime import datetime

@core_bp.route('/')
def index():
    return render_template('index.html')

@core_bp.route('/dashboard')
@login_required
def dashboard():
    websites = Website.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', websites=websites)

@core_bp.route('/generate', methods=['POST'])
@login_required
@limiter.limit("10 per day")
def generate_website():
    try:
        idea = request.form.get('idea')
        if not idea:
            return jsonify({'error': 'Website idea is required'}), 400

        # Create website record
        website = Website(
            name=f"Website-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
            description=idea,
            user_id=current_user.id,
            status='generating'
        )
        db.session.add(website)
        db.session.commit()

        # Initialize website generator with selected model
        llm_type = request.form.get('llm')
        api_key = current_user.api_key  # Use user's stored API key
        
        crew = ModernWebsiteCrew(
            idea=idea,
            llm_type=llm_type,
            api_key=api_key,
            website_id=website.id
        )

        # Generate website
        result = crew.run()

        # Update website record
        website.status = 'completed'
        website.configuration = {
            'llm_type': llm_type,
            'generation_result': result,
            'conversation_log': crew.conversation_log
        }
        db.session.commit()

        return jsonify({
            'message': 'Website generated successfully',
            'website_id': website.id,
            'result': result,
            'conversation_log': crew.conversation_log
        })

    except Exception as e:
        if website:
            website.status = 'failed'
            website.configuration = {
                'error': str(e),
                'llm_type': llm_type
            }
            db.session.commit()
        
        current_app.logger.error(f"Website generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@core_bp.route('/websites/<int:website_id>')
@login_required
def view_website(website_id):
    website = Website.query.get_or_404(website_id)
    if website.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    return render_template('website_details.html', website=website)

@core_bp.route('/websites/<int:website_id>', methods=['DELETE'])
@login_required
def delete_website(website_id):
    website = Website.query.get_or_404(website_id)
    if website.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    db.session.delete(website)
    db.session.commit()
    return jsonify({'message': 'Website deleted successfully'})

@core_bp.route('/websites/<int:website_id>/regenerate', methods=['POST'])
@login_required
@limiter.limit("5 per day")
def regenerate_website(website_id):
    website = Website.query.get_or_404(website_id)
    if website.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        # Update status
        website.status = 'regenerating'
        db.session.commit()

        # Initialize website generator
        crew = ModernWebsiteCrew(
            idea=website.description,
            llm_type=website.configuration.get('llm_type'),
            api_key=current_user.api_key,
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
            'result': result,
            'conversation_log': crew.conversation_log
        })

    except Exception as e:
        website.status = 'failed'
        website.configuration['error'] = str(e)
        db.session.commit()
        
        current_app.logger.error(f"Website regeneration error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@core_bp.route('/websites/<int:website_id>/export', methods=['POST'])
@login_required
@limiter.limit("20 per day")
def export_website(website_id):
    website = Website.query.get_or_404(website_id)
    if website.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        # Implementation for website export functionality
        # This would package up the generated website files
        export_data = {
            'website': website.to_dict(),
            'files': []  # Add logic to collect and package website files
        }
        return jsonify(export_data)
    except Exception as e:
        current_app.logger.error(f"Website export error: {str(e)}")
        return jsonify({'error': str(e)}), 500
