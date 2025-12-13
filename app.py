
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.models import Base, Cliente, Veiculo, OrdemServico, StatusOS
from service.services import UnitOfWork
from service.events import EventLog

app = Flask(__name__)

# Configuração do banco
engine = create_engine("sqlite:///oficina.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
event_log = EventLog()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/clientes")
def listar_clientes():
    clientes = session.query(Cliente).all()
    return render_template("clientes.html", clientes=clientes)

@app.route("/clientes/novo", methods=["POST"])
def novo_cliente():
    nome = request.form["nome"]
    telefone = request.form["telefone"]
    cliente = Cliente(nome=nome, telefone=telefone)
    session.add(cliente)
    session.commit()
    return redirect(url_for("listar_clientes"))

@app.route("/veiculos")
def listar_veiculos():
    veiculos = session.query(Veiculo).all()
    clientes = session.query(Cliente).all()
    return render_template("veiculos.html", veiculos=veiculos, clientes=clientes)

@app.route("/veiculos/novo", methods=["POST"])
def novo_veiculo():
    modelo = request.form["modelo"]
    placa = request.form["placa"]
    cliente_id = request.form["cliente_id"]
    veiculo = Veiculo(modelo=modelo, placa=placa, cliente_id=cliente_id)
    session.add(veiculo)
    session.commit()
    return redirect(url_for("listar_veiculos"))

@app.route("/ordens")
def listar_ordens():
    ordens = session.query(OrdemServico).all()
    veiculos = session.query(Veiculo).all()
    return render_template("ordens.html", ordens=ordens, veiculos=veiculos)

@app.route("/ordens/novo", methods=["POST"])
def nova_ordem():
    descricao = request.form["descricao"]
    valor_estimado = float(request.form["valor_estimado"])
    veiculo_id = request.form["veiculo_id"]
    ordem = OrdemServico(descricao=descricao, valor_estimado=valor_estimado, veiculo_id=veiculo_id)
    session.add(ordem)
    session.commit()
    return redirect(url_for("listar_ordens"))

@app.route("/ordens/<int:id>/status", methods=["POST"])
def alterar_status(id):
    ordem = session.query(OrdemServico).get(id)
    novo_status = request.form["status"]
    if novo_status == "FINALIZADA":
        ordem.valor_final = float(request.form["valor_final"])
    uow = UnitOfWork(session, event_log)
    uow.alterar_status(ordem, StatusOS[novo_status])
    return redirect(url_for("listar_ordens"))

if __name__ == "__main__":
    app.run(debug=True)
