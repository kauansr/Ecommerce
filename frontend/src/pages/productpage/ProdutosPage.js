import axios from 'axios'
import { useState, useEffect } from 'react'
import style from '../../style/produtospagecss/Produtos.module.css'
import { Link } from 'react-router-dom'
import Headers from '../../components/prepaginas/header/Header.js'

function ProdutosPage() {

    const [posts, setPosts] = useState([]);
    const [user, setUser] = useState(null);
    const [filters, setFilters] = useState({
        nome: '',
        categoria: '',
        preco_min: '',
        preco_max: ''
    });

    const getPosts = async (filterParams) => {

        try {
            const tokenauth = localStorage.getItem('token');
            
            const produtosRes = await axios.get("http://127.0.0.1:8000/productapi/produtos/", {
                params: filterParams
            });
            setPosts(produtosRes.data);

    
            const userRes = await axios.get(`http://localhost:8000/accountapi/accounts/`, {
                headers: { 'Authorization': `Bearer ${tokenauth}` }
            });
            setUser(userRes.data);

        } catch (error) {
            console.log('Erro ao carregar os dados', error);
        }

    };

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        setFilters((prevFilters) => ({
            ...prevFilters,
            [name]: value,
        }));
    };

    const handleSearch = () => {
        getPosts(filters);
    };

    useEffect(() => {
        getPosts(filters);
    }, [filters]);

    const links = [
        { path: "/pedidos", label: "Pedidos" },
        { path: '/carrinho', label: 'Carrinho' },
        user ? { path: `/perfil/${user.username}`, label: "Perfil" } : null,
    ].filter(Boolean);

    return (
        <main>
            <Headers links={links} />
            <section className={style.produtospage}>
                <div className={style.filtro}>
                    <h3>Filtrar Produtos</h3>
                    <div>
                        <label>Nome:</label>
                        <input
                            type="text"
                            name="nome"
                            value={filters.nome}
                            onChange={handleFilterChange}
                        />
                    </div>
                    <div>
                        <label>Categoria:</label>
                        <select
                            name="categoria"
                            value={filters.categoria}
                            onChange={handleFilterChange}
                        >
                            <option value="">Selecione</option>
                            <option value="APARELHOS">Aparelhos</option>
                            <option value="ROUPAS">Roupas</option>
                        </select>
                    </div>
                    <div>
                        <label>Preço Mínimo:</label>
                        <input
                            type="number"
                            name="preco_min"
                            value={filters.preco_min}
                            onChange={handleFilterChange}
                        />
                    </div>
                    <div>
                        <label>Preço Máximo:</label>
                        <input
                            type="number"
                            name="preco_max"
                            value={filters.preco_max}
                            onChange={handleFilterChange}
                        />
                    </div>
                    <button onClick={handleSearch}>Filtrar</button>
                </div>

                
                {posts.length === 0 ? (
                    <p>Carregando...</p>
                ) : (
                    posts.map((post) => (
                        <article key={post.id} className={style.produto}>
                            <figure>
                                <img
                                    src={`http://127.0.0.1:8000${post.produto_imagem}`}
                                    alt={post.nome}
                                    width='200'
                                    height='200'
                                />
                            </figure>
                            <div className={style.produtoInfo}>
                                <h2 style={style.nome}>{post.nome}</h2>
                                <p className={style.categoria}>{post.categoria}</p>
                                <p className={style.descricao}>{post.descricao}</p>
                                <p className={style.quantidade}>Estoque: {post.quantidade}</p>
                            </div>
                            <footer>
                                <Link to={`/produto/${post.id}`}>
                                    <button className={style.botao}>R$: {post.preco}</button>
                                </Link>
                            </footer>
                        </article>
                    ))
                )}
            </section>
        </main>
    );
}

export default ProdutosPage;