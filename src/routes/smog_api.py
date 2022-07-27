from flask import Blueprint, Response, jsonify, request
from models.schema import (
    Smog,
)
from peewee import fn

smog_api: Blueprint = Blueprint('smog_api', __name__)


@smog_api.route('/smog/')
@smog_api.route('/smog/<int:id>', methods=['GET'])
def query_smog(id: int | None = None):

    args = request.args
    # TODO: ARE INTS UNSIGNED?
    page: int | None = args.get("page", default=None, type=int)
    per_page: int | None = args.get("per_page", default=5, type=int)
    latest_data: bool | None = args.get("latest", default=False, type=bool)

    result: None | list[Smog] | dict = None
    if id:
        if (
            (smog_select := Smog.select().where(Smog.id == id))
            and
            len(smog_select) == 1
        ):
            smog: Smog = next(iter(smog_select))
            result: dict = smog._data__
        else:
            return Response("{}", status=404, mimetype='application/json')
    else:
        if latest_data:
            result: list[Smog] = [
                smog.__data__ for smog in Smog.select().order_by(
                    (
                        Smog
                        .measurement_timestamp
                        .desc()
                        .limit(
                            Smog.select(fn.Count(fn.Distinct(Smog.site))).scalar()
                        )
                    )
                )
            ]
        elif page:
            per_page = per_page or 5
            # result: list[Smog] = [smog.serialize() for smog in Smog.select().paginate(page, per_page)]
            result: list[Smog] = [smog.__data__ for smog in Smog.select().paginate(page, per_page)]
        else:
            result: list[Smog] = [smog.__data__ for smog in Smog.select()]
            # result: list[Smog] = [smog.serialize() for smog in Smog.select()]

    status: int = 200
    if id:
        status = 200 if result else 404
    return jsonify(
        {
            'smog_data': result,
            'meta': {
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'page_url': request.url,
                }
            }
        }
    ), status
