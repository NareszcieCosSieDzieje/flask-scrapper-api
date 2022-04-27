from flask import Blueprint, Response, jsonify
from scrapping.scrapper import SmogScrapper, GovScrapper, SmogMapScrapper
from ..models.schema import (
    sqlite_db,
    Email,
    Smog,
    smog_factory
)

smog_api: Blueprint = Blueprint('smog_api', __name__)


@smog_api.route('/smog/')
@smog_api.route('/smog/<int:id>', methods=['GET'])  # TODO: PO ID CZY STRING, to i to??
def query_smog(id: int = None):
    # breakpoint()  # FIXME USUN
    # print(Smog._meta.database.get_tables())
    result = None
    if id:
        if (
            (smog_select := Smog.select().where(Smog.id == id))
            and
            len(smog_select) == 1
        ):
            smog: Smog = next(iter(smog_select))
            result: dict = Smog._data__
        # if smog := Smog.get(Smog.id == id):
            # result: Smog = smog.__data__
        else:
            return Response("{}", status=404, mimetype='application/json')
    else:
        result: list[Smog] = [smog.__data__ for smog in Smog.select()]
    return jsonify(result)


@smog_api.route('/emails/', methods=['GET', 'POST'])
@smog_api.route('/emails/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def email_endpoint(id: int = None):
    # name = request.args.get('name')
    result: dict = {}
    if id:
        address: Email = Email.get(Email.id == id)
        if not address:
            return Response("{}", status=404, mimetype='application/json')
    if request.method == 'GET':
        if id:
            query: Email = Email.get(Email.id == id)
        else:
            query: list[Email] = [email.__data__ for email in Email.select()]
        return jsonify(query)
    elif request.method == 'POST':
        if id:
            return Response("{}", status=405, mimetype='application/json')
        else:
            email: Email = Email(request.body)  # FIXME?
            email.save()
            return jsonify(dict(email))
    elif request.method == 'PUT':
        if id:
            query: Email = Email.get(Email.id == id)
            try:
                for k, v in request.body.items():
                    # breakpoint()
                    setattr(query, k, v)  # FIXME CHECK
            # except Peewee.exceptions as e:  # FIXME
            except Exception as e:  # FIXME
                pass
            query.save()
            return jsonify(dict(query))
        else:
            return Response("{}", status=405, mimetype='application/json')
    elif request.method == 'DELETE':
        if id:
            address = Email.get(Email.id == id)
            if address:
                address.delete_instance()
                result = jsonify(address)
            else:
                return Response("{}", status=404, mimetype='application/json')
            return result
        else:
            return Response("{}", status=405, mimetype='application/json')
    else:
        return Response("{}", status=405, mimetype='application/json')

@smog_api.route('/reload_data', methods=['GET'])  # TODO: nazwa?
def reload_data():
    do_smog_scrapping()
    # from datetime import datetime
    # for job in scheduler.get_jobs():
    #     job.modify(next_run_time=datetime.now())
    return Response("{}", status=200, mimetype='application/json')

