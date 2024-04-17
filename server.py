from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine,text
from json import dumps

db_connect = create_engine('mysql+mysqlconnector://root@localhost/monitoramento')

app = Flask(__name__)
api = Api(app)

class Test(Resource):
    def get(self):
        return('{"message":"Servidor funcionando corretamente"}')

class Monitoramento(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute(text('select * from informacao order by temperatura'))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def post(self):
        conn = db_connect.connect()
        temperatura = request.json['temperatura']
        umidade = request.json['umidade']
        dispositivo = request.json['dispositivo']
        conn.execute(text("insert into informacao (temperatura, umidade, dispositivo) values ('{0}', '{1}', '{2}')".format(temperatura, umidade, dispositivo)))
        conn.commit()
        query = conn.execute(text('select * from informacao order by temperatura'))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)
    
    def put(self):
        conn = db_connect.connect()
        id = request.json['id']
        temperatura = request.json['temperatura']
        dispositivo = request.json['dispositivo']
        umidade = request.json['umidade']
        conn.execute(text("update informacao set temperatura ='" + str(temperatura) + "', dispositivo='" + str(dispositivo) + "', umidade ='" + str(umidade) + "'where id = %d " % int(id)))
        conn.commit()
        query = conn.execute(text('select * from informacao order by id'))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

class MonitoramentoById(Resource):
    def delete(self, id):
        conn = db_connect.connect()
        conn.execute( text("delete from informacao where id = %d " % int(id)))
        conn.commit()
        return {"status": "success" }

    def get(self, id ):
        conn = db_connect.connect()
        query = conn.execute(text("select * from informacao where id = %d " % int(id)))
        result = [dict(zip(tuple(query.keys()), i))for i in query.cursor]
        return jsonify(result)
    

api.add_resource(Monitoramento, '/monitoramento')
api.add_resource(MonitoramentoById, '/monitoramentoid/<id>')

if __name__ == '__main__':
    app.run()
