import axios from 'axios'
import { useState, useEffect } from 'react'
import style from '../../style/produtospagecss/Produtos.module.css'
import { useNavigate } from 'react-router-dom'
import { Link } from 'react-router-dom'

function ProdutosPage() {


    const [posts, setPosts] = useState([])

    const navigate = useNavigate()

    const getPosts = async () => {

        try {

            const tokenauth = localStorage.getItem('token')
            const res = await axios.get("http://127.0.0.1:8000/productapi/produtos/", { headers: { 'Authorization': `Bearer ${tokenauth}` } })



            setPosts(res.data)

        } catch (error) {
            console.log(error)

        }


    }


    useEffect(() => {
        getPosts()

    }, [])

    return (

        <div className={style.produtospage}>

            {posts.length === 0 ? <p>Vazio...</p> : (
                posts.map((post) => (
                    <div key={post.id}>

                        <div><img src={`http://127.0.0.1:8000${post.produto_imagem}`} alt={post.produto_imagem} width='100' height='100'></img><div><p>{post.nome}</p></div></div>
                        <div><p>{post.categoria}</p></div>
                        <Link to={`/produto/${post.id}`}><div><button>{post.preco}</button></div> </Link>

                    </div>


                ))
            )

            }

        </div>
    )


}

export default ProdutosPage