import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import style from "../../style/produtospagecss/Carrinho.module.css";
import Headers from '../../components/prepaginas/header/Header';

function Carrinho() {
    const [carrinho, setCarrinho] = useState([]);
    const [total, setTotal] = useState(0);
    const navigate = useNavigate();

    useEffect(() => {
        const carrinhoSalvo = JSON.parse(localStorage.getItem("carrinho")) || [];
        setCarrinho(carrinhoSalvo);
    }, []);

    useEffect(() => {
        
        const totalCarrinho = carrinho.reduce((acc, item) => {
            const preco = item.produto?.preco || 0;  
            const quantidade = item.quantidade || 0; 
            return acc + (preco * quantidade);
        }, 0);
        setTotal(totalCarrinho);
    }, [carrinho]);


    const removerItem = (id) => {
        const novoCarrinho = carrinho.filter((item) => item.produto.id !== id);
        setCarrinho(novoCarrinho);
        localStorage.setItem("carrinho", JSON.stringify(novoCarrinho));
    };

    const finalizarCompra = async () => {
        if (carrinho.length === 0) {
            alert("Seu carrinho está vazio!");
            return;
        }

        const token = localStorage.getItem("token");
        if (!token) {
            alert("Você precisa estar logado para finalizar a compra.");
            navigate("/"); 
            return;
        }

        const itensPedido = carrinho.map((item) => ({
            produto: item.produto.id,
            quantidade: item.quantidade,
        }));

        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/pedidoapi/pedidos/",
                { itens: itensPedido },
                {
                    headers: {
                        "Authorization": `Bearer ${token}`,
                    },
                }
            );

            if (response.status === 201) {
                alert("Compra finalizada com sucesso!");
                setCarrinho([]);
                localStorage.removeItem("carrinho");
                navigate("/pedidos");
            }
        } catch (error) {
            console.error("Erro ao finalizar a compra:", error);
            alert("Erro ao finalizar a compra. Tente novamente.");
        }
    };

    const links = [
        { path: "/pedidos", label: "Pedidos" },
        { path: `/produtos`, label: "Produtos" },
    ];

    return (
        <div>
            <Headers links={links} />
            <div className={style.carrinhoPage}>
                <h1>Carrinho de Compras</h1>
                {carrinho.length === 0 ? (
                    <p>Seu carrinho está vazio.</p>
                ) : (
                    <div>
                        <table className={style.tabelaCarrinho}>
                            <thead>
                                <tr>
                                    <th>Produto</th>
                                    <th>Preço</th>
                                    <th>Quantidade</th>
                                    <th>Total</th>
                                    <th>Remover</th>
                                </tr>
                            </thead>
                            <tbody>
                                {carrinho.map((item) => (
                                    <tr key={item.produto.id}>
                                        <td>{item.produto.nome}</td>
                                        <td>R$: {item.produto.preco?.toFixed(2) || "0.00"}</td>
                                        <td>
                                           {item.quantidade}
                                        </td>
                                        <td>R$: {(item.produto.preco * item.quantidade).toFixed(2) || "0.00"}</td>
                                        <td>
                                            <button onClick={() => removerItem(item.produto.id)}>Remover</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                        <div className={style.totalCarrinho}>
                            <h3>Total: R$: {total.toFixed(2)}</h3>
                        </div>

                        <div className={style.botoesCarrinho}>
                            <button onClick={finalizarCompra}>Finalizar Compra</button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Carrinho;