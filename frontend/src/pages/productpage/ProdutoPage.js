import axios from "axios";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import style from '../../style/produtospagecss/Produto.module.css';
import Headers from '../../components/prepaginas/header/Header.js';

function UmProduto() {
    const [post, setPost] = useState(null);
    const [quantidade, setQuantidade] = useState(1);
    const [carrinho, setCarrinho] = useState([]);  
    const { id } = useParams();  

    const getPost = async () => {
        try {
            const tokenauth = localStorage.getItem('token'); 
            const res = await axios.get(`http://127.0.0.1:8000/productapi/produtos/${id}`, {
                headers: { 'Authorization': `Bearer ${tokenauth}` }, 
            });
            setPost(res.data);
        } catch (error) {
            console.log('Erro ao carregar os dados', error);
        }
    };

    const adicionarAoCarrinho = () => {
        const novoItemCarrinho = {
            produto: post,      
            quantidade: quantidade, 
        };

        setCarrinho((prevCarrinho) => {
            const novoCarrinho = [...prevCarrinho];  
            const indexExistente = novoCarrinho.findIndex((item) => item.produto.id === post.id);  

            if (indexExistente >= 0) {
                
                novoCarrinho[indexExistente].quantidade += quantidade;
            } else {
                
                novoCarrinho.push(novoItemCarrinho);
            }

            
            localStorage.setItem('carrinho', JSON.stringify(novoCarrinho));

            return novoCarrinho;
        });
    };

    useEffect(() => {
        const carrinhoSalvo = JSON.parse(localStorage.getItem('carrinho')) || [];
        setCarrinho(carrinhoSalvo);
    }, []);

    useEffect(() => {
        getPost();
    }, [id]);  

    const handleQuantidadeChange = (e) => {
        let value = e.target.value;

        if (value === "") {
            setQuantidade("");
            return;
        }

        if (!isNaN(value)) {
            value = Math.max(1, Math.min(10, Number(value)));
            setQuantidade(value);
        }
    };

    const links = [
        { path: "/pedidos", label: "Pedidos" },
        { path: `/produtos`, label: "Produtos" },
        { path: '/carrinho', label: 'Carrinho' },
    ];

    return (
        <div>
    <Headers links={links} />
    {post ? (
        <section className={style.produtopage}>
            <article className={style.produto}>
                <figure>
                    <img 
                        src={`http://127.0.0.1:8000${post.produto_imagem}`} 
                        alt={post.nome} 
                        width='150' 
                        height='150' 
                    />
                    
                </figure>
                
                <header>
                    <h2>{post.nome}</h2>
                    <h3>{post.categoria}</h3>
                    <p>{post.descricao}</p>
                </header>

                <section>
                    <h3>Quantidade:</h3>
                    <input
                        type="number"
                        id="quantidade"
                        name="quantidade"
                        max="10"
                        value={quantidade}
                        onChange={handleQuantidadeChange}
                    />
                </section>
                
                <footer>
                    <h3>R$: {post.preco}</h3>
                    <form onSubmit={(e) => e.preventDefault()}>
                        <button type="button" onClick={adicionarAoCarrinho}>
                            Adicionar ao Carrinho
                        </button>
                    </form>
                </footer>
            </article>
        </section>
    ) : (
        <p>Vazio...</p>
    )}
</div>
    );
}

export default UmProduto;