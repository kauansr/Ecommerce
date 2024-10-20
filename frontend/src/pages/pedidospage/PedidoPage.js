import axios from "axios";
import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import style from '../../style/pedidospagecss/Pedido.module.css';
import Headers from '../../components/prepaginas/header/Header.js'

function UmPedido() {
    const [post, setPost] = useState(null);
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const { id } = useParams();

    const getPost = async () => {
        try {
            const tokenauth = localStorage.getItem('token');
            const res = await axios.get(`http://127.0.0.1:8000/pedidoapi/pedidos/${id}`, {
                headers: { 'Authorization': `Bearer ${tokenauth}` }
            });
            setPost(res.data);
        } catch (error) {
            setError("Erro ao carregar o pedido.");
        }
    };

    useEffect(() => {
        getPost();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const tokenauth = localStorage.getItem('token');

        try {
            await axios.delete(`http://127.0.0.1:8000/pedidoapi/pedidos/${id}`, {
                headers: { 'Authorization': `Bearer ${tokenauth}` }
            });
            navigate("/pedidos");
        } catch (err) {
            setError("Erro ao cancelar o pedido."); 
        }
    };

    const links = [
        { path: "/pedidos", label: "Pedidos" },
        { path: `/produtos`, label: "Produtos" },
    ];

    return (
        <div>
            <Headers links={links}/>
            {error && <p>{error}</p>} {}
            {!post ? (
                <p>Vazio...</p>
            ) : (
                <div className={style.pedidospage}>
                    <h2>{post.nome_pedido}</h2>
                    <h3>Status: {post.entrega_status}</h3>
                    <h3>Destinatário: {post.email}</h3>
                    <h3>R$: {post.preco}</h3>
                    <br />
                    <form onSubmit={handleSubmit}>
                        <div>
                            <button type="submit">Cancelar</button>
                        </div>
                    </form>
                    <br />
                </div>
            )}
        </div>
    );
}

export default UmPedido;