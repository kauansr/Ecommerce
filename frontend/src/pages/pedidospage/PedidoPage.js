import axios from "axios";
import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import style from '../../style/pedidospagecss/Pedido.module.css';
import Headers from '../../components/prepaginas/header/Header.js';

function UmPedido() {
    const [post, setPost] = useState(null);
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const { id } = useParams(); 

   
    const getPost = async () => {
        try {
            const tokenauth = localStorage.getItem('token');
            if (!tokenauth) {
                setError("Token de autenticação não encontrado.");
                return;
            }

            const res = await axios.get(`http://127.0.0.1:8000/pedidoapi/pedidos/${id}`, {
                headers: { 'Authorization': `Bearer ${tokenauth}` }
            });
            setPost(res.data);
        } catch (error) {
            setError("Erro ao carregar o pedido. Tente novamente mais tarde.");
        }
    };

    
    const handleSubmit = async (e) => {
        e.preventDefault();
        const tokenauth = localStorage.getItem('token');
        if (!tokenauth) {
            setError("Token de autenticação não encontrado.");
            return;
        }

        try {
            await axios.delete(`http://127.0.0.1:8000/pedidoapi/pedidos/${id}`, {
                headers: { 'Authorization': `Bearer ${tokenauth}` }
            });
            navigate("/pedidos");
        } catch (err) {
            setError("Erro ao cancelar o pedido. Tente novamente.");
        }
    };


    const links = [
        { path: "/pedidos", label: "Pedidos" },
        { path: "/produtos", label: "Produtos" },
        { path: '/carrinho', label: 'Carrinho' },
    ];

    useEffect(() => {
        getPost();
    }, [id]); 

    return (
        <div>
            <Headers links={links} />
            {error && <p className={style.error}>{error}</p>}
            {!post ? (
                <p>Carregando...</p>
            ) : (
                <div className={style.pedidospage}>
                    <h2>Pedido de: {post.pedido.email}</h2>
                    <h3>Status: {post.pedido.entrega_status}</h3>
                    <h3>Destinatário: {post.pedido.email}</h3>
                    <h3>Total: R$ {post.pedido.total}</h3>

                    <h4>Itens do Pedido:</h4>
                    <ul>
                        {post.itens && post.itens.map((item, index) => (
                            <li key={index} className={style.itemPedido}>
                                <div className={style.itemImageWrapper}>
                                    <img 
                                        src={`http://127.0.0.1:8000/${item.produto_imagem}`} 
                                        alt={item.produto_nome} 
                                        className={style.itemImage}
                                    />
                                </div>
                                <div className={style.itemDetails}>
                                    <strong>Produto:</strong> {item.produto_nome} <br />
                                    <strong>Quantidade:</strong> {item.quantidade} <br />
                                    <strong>Preço Unitário:</strong> R$ {item.preco_unitario} <br />
                                </div>
                            </li>
                        ))}
                    </ul>

                    <br />
                    <form onSubmit={handleSubmit}>
                        <div>
                            <button type="submit">Cancelar Pedido</button>
                        </div>
                    </form>
                </div>
            )}
        </div>

    );
}

export default UmPedido;