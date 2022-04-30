from flask import Blueprint, Response, jsonify, request
from models.schema import Email

email_api: Blueprint = Blueprint('email_api', __name__)


# TODO: fix and develop mailing
# @email_api.route('/emails/', methods=['GET', 'POST'])
# @email_api.route('/emails/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# def email_endpoint(id: int = None):
#     # name = request.args.get('name')
#     result: dict = {}
#     if id:
#         address: Email = Email.get(Email.id == id)
#         if not address:
#             return Response("{}", status=404, mimetype='application/json')
#     if request.method == 'GET':
#         if id:
#             query: Email = Email.get(Email.id == id)
#         else:
#             query: list[Email] = [email.__data__ for email in Email.select()]
#         return jsonify(query)
#     elif request.method == 'POST':
#         if id:
#             return Response("{}", status=405, mimetype='application/json')
#         else:
#             email: Email = Email(request.body)  # FIXME?
#             email.save()
#             return jsonify(dict(email))
#     elif request.method == 'PUT':
#         if id:
#             query: Email = Email.get(Email.id == id)
#             try:
#                 for k, v in request.body.items():
#                     # breakpoint()
#                     setattr(query, k, v)  # FIXME CHECK
#             # except Peewee.exceptions as e:  # FIXME
#             except Exception as e:  # FIXME
#                 pass
#             query.save()
#             return jsonify(dict(query))
#         else:
#             return Response("{}", status=405, mimetype='application/json')
#     elif request.method == 'DELETE':
#         if id:
#             address = Email.get(Email.id == id)
#             if address:
#                 address.delete_instance()
#                 result = jsonify(address)
#             else:
#                 return Response("{}", status=404, mimetype='application/json')
#             return result
#         else:
#             return Response("{}", status=405, mimetype='application/json')
#     else:
#         return Response("{}", status=405, mimetype='application/json')
