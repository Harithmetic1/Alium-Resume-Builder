from app.main import main
from flask import jsonify
from flask_login import current_user
from app import db
from app.models import Education, Skill, Hobbies, Languages, Experience


@main.route('/api/<type>', methods=['GET'])
def get_details(type):
    dict_ = {
        'skill': current_user.skills.all(),
        'languages': current_user.languages.all(),
        'education': current_user.educations.all(),
        'experience': current_user.works.all(),
        'hobbies': current_user.hobbies.all()
    }
    user_data = dict_.get(type)
    if user_data:
        user_data = [data.get_json() for data in user_data]
    else:
        abort(404)
    return jsonify({
        'result': user_data
    }) 

@main.route('/api/<type>', methods=['POST'])
def create_details(type):
    dict_ = {
        'skill': current_user.skills,
        'languages': current_user.languages,
        'education': current_user.educations,
        'experience': current_user.works,
        'hobbies': current_user.hobbies
    }
    dict_1 = {
        'skill': Skill,
        'languages': Languages,
        'education': Education,
        'experience': Experience,
        'hobbies': Hobbies
    }
    data = request.get_json()
    user_data = dict_.get(type)
    if user_data:
        try:
            new = dict_1.get(type)
            if new:
                d = new()
                d.create_data(data)
                db.session.add(d)
                db.session.commit()
                d.users.append(current_user)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': 'Something went wrong, might be that you passed the wrong data',
                'message': e
            })
    else:
        abort(404)
    return jsonify({
        'result': 'Data Created'
    }), 204

@main.route('/api/<type>/<name>', methods=['PUT'])
def update_details(type, name):
    dict_ = {
        'skill': current_user.skills,
        'languages': current_user.languages,
        'education': current_user.educations,
        'experience': current_user.works,
        'hobbies': current_user.hobbies
    }
    data = request.get_json()
    user_data = dict_.get(type)
    if user_data:
        try:
            new = dict_.get(type)
            if new:
                if type == 'skill' or type == 'hobbies' or type == 'languages':
                    d = new.filter_by(name=name).first()
                elif type == 'educations':
                    d = new.filter_by(course=name).first()
                elif type == 'experience':
                    d = new.filter_by(title=name).first()
                else:
                    abort(404)
                d.create_data(data)
                db.session.add(d)
                db.session.commit()
                d.users.append(current_user)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': 'Something went wrong, might be that you passed the wrong data',
                'message': e
            })
    else:
        abort(404)
    return jsonify({
        'result': 'Data Updated'
    }), 204

@main.route('/api/<type>/<name>', methods=['DELETE'])
def delete_details(type, name):
    dict_ = {
        'skill': current_user.skills,
        'languages': current_user.languages,
        'education': current_user.educations,
        'experience': current_user.works,
        'hobbies': current_user.hobbies
    }
    data = request.get_json()
    user_data = dict_.get(type)
    if user_data:
        try:
            new = dict_.get(type)
            if new:
                if type == 'skill' or type == 'hobbies' or type == 'languages':
                    d = new.filter_by(name=name).first()
                elif type == 'educations':
                    d = new.filter_by(course=name).first()
                elif type == 'experience':
                    d = new.filter_by(title=name).first()
                else:
                    abort(404)
                db.session.delete(d)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': 'Something went wrong, might be that you passed the wrong data',
                'message': e
            })
    else:
        abort(404)
    return jsonify({
        'result': 'Data Created'
    }), 204