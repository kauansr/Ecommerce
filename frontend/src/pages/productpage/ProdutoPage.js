import axios from "axios";
import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import style from '../../style/produtospagecss/Produto.module.css';
import Headers from '../../components/prepaginas/header/Header.js';

function UmProduto() {
    const [post, setPost] = useState(null);
    const navigate = useNavigate();
    const { id } = useParams();

    const getPost = async () => {
        try {
            const tokenauth = localStorage.getItem('token');

            
            const res = await axios.get(`http://localhost:8000/productapi/produtos/${id}`);
            setPost(res.data);

        } catch (error) {
            console.log('Erro ao carregar os dados', error);
        }
    };

    useEffect(() => {
        getPost();
    }, []);

    const handleSubmit = async (data) => {
        data.preventDefault();
        const tokenauth = localStorage.getItem('token');

        try {
            await axios.post(`http://127.0.0.1:8000/pedidoapi/pedidos/`, { id: id }, {
                headers: { 'Authorization': `Bearer ${tokenauth}` }
            });
            navigate("/pedidos");
        } catch (err) {
            console.log('Erro ao fazer pedido', err);
        }
    };

    const links = [
        { path: "/pedidos", label: "Pedidos" },
        { path: `/produtos`, label: "Produtos" },
    ];

    return (
        <div>
            <Headers links={links} />
            {post ? (
                <div className={style.produtopage}>
                    <div key={post.id} className={style.produto}>
                        <img 
                            src={`http://127.0.0.1:8000${post.produto_imagem}`} 
                            alt={post.nome} 
                            width='100' 
                            height='100' 
                        />
                        <h2>{post.nome}</h2>
                        <h3>{post.categoria}</h3>
                        <h3>{post.descricao}</h3>
                        <h3>R$: {post.preco}</h3>
                        <form onSubmit={handleSubmit}>
                            <button type="submit">Pedir</button>
                        </form>
                    </div>
                </div>
            ) : (
                <p>Vazio...</p>
            )}
        </div>
    );
}

export default UmProduto;