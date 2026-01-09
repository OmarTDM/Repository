import graphene
from graphene.types.generic import GenericScalar
from db import db, projects_collection
from bson.objectid import ObjectId


def _to_jsonable(doc):
    """Turn a Mongo document into something we can safely JSON-encode."""
    import base64

    def sanitize_value(v):
        # Mongo ObjectId doesn't serialize to JSON, so stringify it.
        try:
            if hasattr(v, '__class__') and v.__class__.__name__ == 'ObjectId':
                return str(v)
        except Exception:
            pass
        # Some documents may contain raw bytes (e.g., images). Try UTF-8 first;
        # if that fails, fall back to base64.
        if isinstance(v, (bytes, bytearray)):
            try:
                return v.decode('utf-8')
            except Exception:
                return base64.b64encode(bytes(v)).decode('ascii')
        # Walk nested structures so everything becomes JSON-friendly.
        if isinstance(v, dict):
            return {kk: sanitize_value(vv) for kk, vv in v.items()}
        # Same idea for arrays.
        if isinstance(v, (list, tuple)):
            return [sanitize_value(x) for x in v]
        # Plain values (str/int/float/bool/None) are fine as-is.
        return v

    if doc is None:
        return None
    out = {}
    for k, v in doc.items():
        if k == '_id':
            out['id'] = str(v)
        else:
            out[k] = sanitize_value(v)
    return out


class Query(graphene.ObjectType):
    """A tiny, flexible GraphQL layer over MongoDB.

    Everything returns JSON-ish data via GenericScalar so the frontend can pick
    fields dynamically.
    """

    # List the collections in the database.
    collections = graphene.List(graphene.String)

    # Grab a handful of docs (useful for discovering fields).
    sample_documents = graphene.List(GenericScalar, collection=graphene.String(required=True), limit=graphene.Int())

    # A generic find() with optional filter/projection/limit.
    query_documents = graphene.List(GenericScalar, collection=graphene.String(required=True), filter=GenericScalar(), projection=GenericScalar(), limit=graphene.Int())

    # Distinct values for a single field.
    distinct = graphene.List(GenericScalar, collection=graphene.String(required=True), field=graphene.String(required=True))

    # Configuration documents used to define dynamic_<id> custom fields.
    configurations = graphene.List(
        GenericScalar,
        connected_collection=graphene.String(),
        inuse=graphene.Boolean(),
    )

    # Resolve a list of Mongo document ids to a display label.
    # Useful for turning ObjectId strings shown in charts into human names.
    lookup_labels = graphene.List(
        GenericScalar,
        collection=graphene.String(required=True),
        ids=graphene.List(graphene.String, required=True),
        label_field=graphene.String(),
    )

    def resolve_collections(self, info):
        if db is None:
            return []
        return list(db.list_collection_names())

    def resolve_sample_documents(self, info, collection, limit=10):
        if db is None:
            return []
        coll = db[collection]
        docs = list(coll.find({}, limit=limit))
        return [_to_jsonable(d) for d in docs]

    def resolve_query_documents(self, info, collection, filter=None, projection=None, limit=0):
        # filter/projection come from the client as JSON like objects.
        if db is None:
            return []
        coll = db[collection]
        _filter = filter or {}
        _projection = projection or None
        try:
            if limit and isinstance(limit, int) and limit > 0:
                docs = list(coll.find(_filter, _projection).limit(limit))
            else:
                docs = list(coll.find(_filter, _projection))
        except Exception:
            # If the client sends a bad filter/projection, just return nothing.
            docs = []
        return [_to_jsonable(d) for d in docs]

    def resolve_distinct(self, info, collection, field):
        if db is None:
            return []
        coll = db[collection]
        try:
            vals = coll.distinct(field)
        except Exception:
            vals = []
        return vals

    # READS DYNAMICS IN DATABASE !!!
    def resolve_configurations(self, info, connected_collection=None, inuse=None):
        if db is None:
            return []
        try:
            coll = db["configurations"]
        except Exception:
            return []

        q = {}
        if connected_collection:
            q["ConnectedCollection"] = connected_collection
        if inuse is not None:
            q["inuse"] = bool(inuse)

        try:
            docs = list(coll.find(q))
        except Exception:
            docs = []
        return [_to_jsonable(d) for d in docs]

    def resolve_lookup_labels(self, info, collection, ids, label_field=None):
        if db is None:
            return []
        if not ids:
            return []
        try:
            coll = db[collection]
        except Exception:
            return []

        # Convert parseable ObjectId strings; keep non-ObjectId ids as-is.
        obj_ids = []
        raw_ids = []
        for s in ids:
            if s is None:
                continue
            ss = str(s)
            try:
                obj_ids.append(ObjectId(ss))
            except Exception:
                raw_ids.append(ss)

        by_id = {}
        if obj_ids:
            try:
                for d in coll.find({"_id": {"$in": obj_ids}}):
                    by_id[str(d.get("_id"))] = d
            except Exception:
                pass
        if raw_ids:
            try:
                for d in coll.find({"_id": {"$in": raw_ids}}):
                    by_id[str(d.get("_id"))] = d
            except Exception:
                pass

        def pick_label(doc):
            if not doc:
                return None
            if label_field and label_field in doc:
                v = doc.get(label_field)
                if v is not None:
                    s = str(v).strip()
                    if s:
                        return s
            # Fall back to common label fields.
            for k in ("title", "name", "research_project", "research_project_code"):
                if k in doc and doc.get(k) is not None:
                    s = str(doc.get(k)).strip()
                    if s:
                        return s
            return None

        out = []
        for s in ids:
            if s is None:
                continue
            sid = str(s)
            doc = by_id.get(sid)
            label = pick_label(doc) or sid
            out.append({"id": sid, "label": label})
        return out


schema = graphene.Schema(query=Query, auto_camelcase=True)