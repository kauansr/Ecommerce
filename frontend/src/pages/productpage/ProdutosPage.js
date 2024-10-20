import axios from 'axios'
import { useState, useEffect } from 'react'
import style from '../../style/produtospagecss/Produtos.module.css'
import { useNavigate, useParams } from 'react-router-dom'
import { Link } from 'react-router-dom'
import Headers from '../../components/prepaginas/header/Header.js'

function ProdutosPage() {


    const [posts, setPosts] = useState([])
    const [user, setUser] = useState(null)

    const navigate = useNavigate()

    const getPosts = async () => {

        try {

            const tokenauth = localStorage.getItem('token');

            
            const produtosRes = await axios.get("http://127.0.0.1:8000/productapi/produtos/");
            setPosts(produtosRes.data);


            const userRes = await axios.get(`http://localhost:8000/accountapi/accounts/`, {
                headers: { 'Authorization': `Bearer ${tokenauth}` }
            });
            setUser(userRes.data);
        } catch (error) {
            console.log('Erro ao carregar os dados', error);
        }

    }



    useEffect(() => {
        getPosts()
    }, [])

    const links = [
        { path: "/pedidos", label: "Pedidos" },
        user ? { path: `/perfil/${user.username}`, label: "Perfil" } : null,
    ].filter(Boolean);

    return (
        <div>
            <Headers links={links}/>
        <div className={style.produtospage}>
            {posts.length === 0 ? (
                <p>Carregando...</p>
            ) : (
                posts.map((post) => (
                    <div key={post.id} className={style.produto}>
                        <img 
                            src={`http://127.0.0.1:8000${post.produto_imagem}`} 
                            alt={post.nome} 
                            width='100' 
                            height='100' 
                        />
                        <p className={style.nome}>{post.nome}</p>
                        <p className={style.categoria}>{post.categoria}</p>
                        <p className={style.descricao}>{post.descricao}</p>
                        <Link to={`/produto/${post.id}`}>
                            <button className={style.botao}>R$: {post.preco}</button>
                        </Link>
                    </div>
                ))
            )}
        </div>
        </div>
    );


}

export default ProdutosPage