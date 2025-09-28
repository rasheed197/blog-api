from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flasgger import swag_from

from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from src.database import Post, db

posts_bp = Blueprint("posts", __name__, url_prefix="/api/v1/post")


@posts_bp.route("/", methods=["POST"])
@jwt_required()
def posts():
    author_id = get_jwt_identity()

    data = request.get_json()

    title = data.get("title", "")
    content = data.get("content", "")

    if not title or not content:
        return (
            jsonify({"error": "title and content are required"}),
            HTTP_400_BAD_REQUEST,
        )

    post = Post(title=title, content=content, author_id=author_id)
    db.session.add(post)
    db.session.commit()

    return (
        jsonify(
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "slug": post.slug,
                "author": {"id": post.author_id, "username": post.author.username},
                "created_at": post.created_at,
                "updated_at": post.updated_at,
            }
        ),
        HTTP_201_CREATED,
    )


@posts_bp.get("/")
def get_posts():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    posts = Post.query.paginate(page=page, per_page=per_page, error_out=True)

    data = [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "slug": post.slug,
            "author": {
                "id": post.author.id,
                "username": post.author.username,
            },
            "created_at": post.created_at,
            "updated_at": post.updated_at,
        }
        for post in posts.items
    ]

    meta = {
        "page": posts.page,
        "pages": posts.pages,
        "total_count": posts.total,
        "prev_page": posts.prev_num,
        "next_page": posts.next_num,
        "has_next": posts.has_next,
        "has_prev": posts.has_prev,
    }

    return (
        jsonify({"data": data, "meta": meta}),
        HTTP_200_OK,
    )


@posts_bp.get("/<int:id>")
def get_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        return jsonify({"error": "Post not foundd"}), HTTP_404_NOT_FOUND

    return (
        jsonify(
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "slug": post.slug,
                "author": {
                    "id": post.author.id,
                    "username": post.author.username,
                },
                "created_at": post.created_at,
                "updated_at": post.updated_at,
            }
        ),
        HTTP_200_OK,
    )


@posts_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_post(id):
    author_id = get_jwt_identity()

    post = Post.query.filter_by(author_id=author_id, id=id).first()
    if not post:
        return jsonify({"error": "Post not foundd"}), HTTP_404_NOT_FOUND

    data = request.get_json()

    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)

    db.session.commit()

    return (
        jsonify(
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "slug": post.slug,
                "author": {"id": post.author_id, "username": post.author.username},
                "created_at": post.created_at,
                "updated_at": post.updated_at,
            }
        ),
        HTTP_200_OK,
    )


@posts_bp.delete("/<int:id>")
@jwt_required()
@swag_from('../docs/posts/delete.yaml')
def delete_post(id):
    author_id = get_jwt_identity()

    post = Post.query.filter_by(author_id=author_id, id=id).first_or_404()
    
    if not post:
        return jsonify({"error": "Post not foundd"}), HTTP_404_NOT_FOUND

    db.session.delete(post)
    db.session.commit()

    return (
        jsonify({}),
        HTTP_204_NO_CONTENT,
    )
