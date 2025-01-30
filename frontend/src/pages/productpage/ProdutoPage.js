import axios from "axios";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import style from '../../style/produtospagecss/Produto.module.css';
import Headers from '../../components/prepaginas/header/Header.js';

function UmProduto() {
    const [post, setPost] = useState(null);
    const [quantidade, setQuantidade] = useState(1);
    const [comentario, setComentario] = useState('');
    const [carrinho, setCarrinho] = useState([]);
    const [nota, setNota] = useState(1);
    const [comentarios, setComentarios] = useState([]);
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

   
    const getComentarios = async () => {
        try {
            const tokenauth = localStorage.getItem('token');
            const res = await axios.get(`http://127.0.0.1:8000/productapi/avaliacoes/${id}/`, {
                headers: { 'Authorization': `Bearer ${tokenauth}` },
            });
            setComentarios(res.data); 
        } catch (error) {
            console.log('Erro ao carregar os comentários', error);
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

    const adicionarAvaliacao = async (e) => {
        e.preventDefault();
        const tokenauth = localStorage.getItem('token');
        
        const novaAvaliacao = {
            produto: post.id,
            comentario: comentario,
            nota: nota,
        };

        try {
            await axios.post(`http://127.0.0.1:8000/productapi/avaliacoes/${id}/`, novaAvaliacao, {
                headers: { 'Authorization': `Bearer ${tokenauth}` },
            });
            alert('Avaliação enviada!');
            setComentario('');
            setNota(1); 
            getComentarios();
        } catch (error) {
            console.error('Erro ao enviar avaliação:', error);
        }
    };

    useEffect(() => {
        getPost();
        getComentarios();
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

    const handleStarClick = (rating) => {
        setNota(rating); 
    };

    const renderStars = () => {
        let stars = [];
        for (let i = 1; i <= 5; i++) {
            stars.push(
                <span
                    key={i}
                    className={i <= nota ? style.starSelected : style.star}
                    onClick={() => handleStarClick(i)}
                >
                    &#9733; 
                </span>
            );
        }
        return stars;
    };

    return (
        <div>
            <Headers links={[{ path: "/produtos", label: "Produtos" }, { path: "/carrinho", label: "Carrinho" }]} />
            {post ? (
                <section className={style.produtopage}>
                    <article className={style.produto}>
                        <figure>
                            <img src={`http://127.0.0.1:8000${post.produto_imagem}`} alt={post.nome} width='150' height='150' />
                        </figure>
                        <header>
                            <h2>{post.nome}</h2>
                            <h3>{post.categoria}</h3>
                            <p>{post.descricao}</p>
                        </header>
                        <section>
                            <h3>Quantidade:</h3>
                            <input type="number" id="quantidade" name="quantidade" max="10" value={quantidade} onChange={handleQuantidadeChange} />
                        </section>
                        <footer>
                            <h3>R$: {post.preco}</h3>
                            <form onSubmit={(e) => e.preventDefault()}>
                                <button type="button" onClick={adicionarAoCarrinho}>Adicionar ao Carrinho</button>
                            </form>
                        </footer>
                    </article>

                    <section className={style.avaliacaoSection}>
                        <h3>Avaliação do Produto</h3>
                        <div className={style.stars}>
                            {renderStars()} 
                        </div>

                        <form onSubmit={adicionarAvaliacao}>
                            <textarea
                                value={comentario}
                                onChange={(e) => setComentario(e.target.value)}
                                placeholder="Deixe seu comentário..."
                                required
                            />
                            <button type="submit">Enviar Avaliação</button>
                        </form>
                    </section>

                    
                    <section className={style.comentariosSection}>
                        <h3>Comentários</h3>
                        {comentarios.length > 0 ? (
                            <ul>
                                {comentarios.map((comentario, index) => (
                                    <li key={index}>
                                        <p><strong>{comentario.usuario_nome}</strong></p>
                                        <p>{comentario.comentario}</p>
                                        <div>{'★'.repeat(comentario.estrelas)}</div>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p>Não há comentários ainda.</p>
                        )}
                    </section>
                </section>
            ) : (
                <p>Vazio...</p>
            )}
        </div>
    );
}

export default UmProduto;