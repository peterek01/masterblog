from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def generate_new_id():
    """
    Generates a new unique ID for a post.
    """
    if POSTS:
        return max(post["id"] for post in POSTS) + 1
    return 1


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Handles GET requests to list all posts with optional sorting.
    Query parameters:
      - sort: Field to sort by ('title' or 'content').
      - direction: Sort order ('asc' or 'desc').
    """
    sort_field = request.args.get('sort', None)
    sort_direction = request.args.get('direction', 'asc').lower()

    # Validate sort field and direction
    if sort_field and sort_field not in ['title', 'content']:
        return jsonify({"error": f"Invalid sort field: {sort_field}. Valid options are 'title' or 'content'."}), 400

    if sort_direction not in ['asc', 'desc']:
        return jsonify({"error": f"Invalid sort direction: {sort_direction}. Valid options are 'asc' or 'desc'."}), 400

    sorted_posts = POSTS[:]

    # Apply sorting if sort_field is provided
    if sort_field:
        reverse = sort_direction == 'desc'
        sorted_posts.sort(key=lambda post: post.get(sort_field, '').lower(), reverse=reverse)

    return jsonify(sorted_posts), 200


@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    if request.method == 'GET':
        # Sorting logic (as implemented previously)
        sort_field = request.args.get('sort', None)
        sort_direction = request.args.get('direction', 'asc').lower()

        if sort_field and sort_field not in ['title', 'content']:
            return jsonify({"error": f"Invalid sort field: {sort_field}. Valid options are 'title' or 'content'."}), 400

        if sort_direction not in ['asc', 'desc']:
            return jsonify({"error": f"Invalid sort direction: {sort_direction}. Valid options are 'asc' or 'desc'."}), 400

        sorted_posts = POSTS[:]
        if sort_field:
            reverse = sort_direction == 'desc'
            sorted_posts.sort(key=lambda post: post.get(sort_field, '').lower(), reverse=reverse)

        return jsonify(sorted_posts), 200

    elif request.method == 'POST':
        # Add new post logic
        new_post = request.get_json()
        if 'title' not in new_post or 'content' not in new_post:
            return jsonify({"error": "Both title and content are required."}), 400

        new_id = max(post['id'] for post in POSTS) + 1
        new_post['id'] = new_id
        POSTS.append(new_post)
        return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """
    Deletes a blog post by its ID.
    """
    post_to_delete = next((post for post in POSTS if post["id"] == id), None)

    if not post_to_delete:
        return jsonify({"error": f"Post with id {id} not found."}), 404

    POSTS.remove(post_to_delete)
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """
    Updates an existing blog post by ID.
    Expects a JSON payload with optional 'title' and 'content'.
    """
    post_to_update = next((post for post in POSTS if post["id"] == id), None)

    if not post_to_update:
        return jsonify({"error": f"Post with id {id} not found."}), 404

    new_data = request.get_json()
    post_to_update["title"] = new_data.get("title", post_to_update["title"])
    post_to_update["content"] = new_data.get("content", post_to_update["content"])

    return jsonify(post_to_update), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Searches for blog posts by title or content.
    Expects 'title' and/or 'content' as query parameters.
    """
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    filtered_posts = [
        post for post in POSTS
        if (title_query in post['title'].lower() if title_query else True) and
           (content_query in post['content'].lower() if content_query else True)
    ]

    return jsonify(filtered_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
