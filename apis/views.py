import copy
import hashlib

from flask import Blueprint , request , jsonify
from sqlalchemy.orm.attributes import flag_modified

from apis.models import Stories , db , UserIdentities
from apis.utils import authenticate_request

stories = Blueprint('stories', __name__, )


@stories.route('/signup_author', methods=['POST'])
def signup():
    data = request.get_json()
    mobile = data.get('mobile')
    password = data.get('password')
    if not mobile:
        return jsonify({'result': 'error', 'message': 'Require mobile'}), 200
    if not password:
        return jsonify({'result': 'error', 'message': 'Enter password'}) , 200
    if not data.get('name'):
        return jsonify({'result': 'error', 'message': 'Enter your name'}), 200
    name = data.get('name')

    password = hashlib.sha256(password.encode()).hexdigest()
    UserIdentities.new(identity=mobile, identity_type='Author', password=password, row_status='active', name=name)
    db.session.commit()
    return jsonify({'result': 'success', 'message': 'Draft saved successfully'})


@stories.route('/add_new_stories', methods=['POST'])
@authenticate_request()
def add_story_as_draft(who):
    author = who
    data = request.get_json()
    if not data:
        return jsonify({'result': 'error', 'message': 'No data'}), 200
    draft = data.get('draft')
    title = data.get('title')
    if not title:
        return jsonify({'result': 'error', 'message': 'Require title'}), 200
    tags = data.get('tags')
    if tags and not isinstance(tags, list):
        tags = tags.split(",")
    if_publiced = False
    if data.get('if_publice') is True:
        if_publiced = True
    Stories.new(draft=draft, title=title, tags=tags, if_publiced=if_publiced, performed_by=author)
    db.session.commit()
    return jsonify({'result': 'success', 'message': 'Draft saved successfully'})


@stories.route('/edit_story', methods=['POST'])
@authenticate_request()
def edit_story(who):
    author = who
    data = request.get_json()
    if not data:
        return jsonify({'result': 'error', 'message': 'No data'}), 200
    draft_id = data.get('id')
    story = Stories.get(Stories.id == draft_id)
    if story.performed_by != author:
        return jsonify({'result': 'error', 'message': 'Can not edit the story'}), 200
    if data.get('is_delete') is True:
        story.row_status = 'inactive'
    else:
        if data.get('title'):
            story.title = data.get('title')
        if data.get('draft'):
            story.draft = data.get('draft')
        tags = data.get('tags')
        if tags:
            if not isinstance(tags , list):
                tags = tags.split(",")
            existing_tags = set(story.tags)
            story.tags = list(existing_tags | set(tags))
        if data.get('if_publice') in [True, False]:
            story.if_publiced = data.get('if_publice')
    db.session.commit()
    return jsonify({'result': 'success', 'message': 'Draft saved successfully'})


@stories.route('/get_stories', methods=['GET'])
@authenticate_request()
def get_all_stories(who):
    author = who
    filters = []
    tags = request.args.getlist('tags')
    if tags:
        filters.append(Stories.tags.in_(tags))
    title = request.args.get('title')
    if title:
        filters.append(Stories.title.ilike("%" + title + "%"))
    context = request.args.get('context')
    if context:
        filters.append(Stories.draft.ilike("%" + context + "%"))

    Query = db.session.query(Stories).filter(*filters)
    if request.args.get('order_by') == 'created_at_desc':
        Query = Query.order_by(Stories.created_at.desc())
    elif request.args.get('order_by') == 'created_at_asc':
        Query = Query.order_by(Stories.created_at)
    elif request.args.get('order_by') == 'updated_at_desc':
        Query = Query.order_by(Stories.updated_at.desc())
    elif request.args.get('order_by') == 'updated_at_asc':
        Query = Query.order_by(Stories.updated_at)
    elif request.args.get('order_by') == 'title_asc':
        Query = Query.order_by(Stories.title)
    elif request.args.get('order_by') == 'title_desc':
        Query = Query.order_by(Stories.title.desc())

    draft = Query.filter(Stories.if_publiced == False, Stories.performed_by == author).all()
    author_name = request.args.get('author')
    if author_name:
        author_id = db.session.query(UserIdentities.id).filter(UserIdentities.identity_type == 'Author' ,
                                                               UserIdentities.row_status == 'active' ,
                                                               UserIdentities.name.ilike("%" + author_name +
                                                                                         "%")).subquery()
        filters.append(Stories.performed_by.in_(author_id))
    publiced_stories = Query.filter(Stories.if_publiced == True).all()
    if publiced_stories:
        publiced_stories = [publiced_story.as_dict() for publiced_story in publiced_stories]
    else:
        publiced_stories = []
    if draft:
        draft = [x.as_dict() for x in draft]
    else:
        draft = []

    return jsonify({'result': 'success', 'publiced_stories': publiced_stories, 'drafts': draft})