import axios from 'axios'
import { useState, useEffect } from 'react'
import style from '../../style/pedidospagecss/Pedidopage.module.css'
import { Link } from 'react-router-dom'
import Headers from '../../components/prepaginas/header/Header.js'

function PedidosPage() {


    const [posts, setPosts] = useState([])

    const getPosts = async () => {

        try {

            const tokenauth = localStorage.getItem('token')
            const res = await axios.get("http://127.0.0.1:8000/pedidoapi/pedidos/", { headers: { 'Authorization': `Bearer ${tokenauth}` } })



            setPosts(res.data)

        } catch (error) {
            console.log(error)

        }


    }


    useEffect(() => {
        getPosts()

    }, [])

    const links = [
        { path: `/produtos`, label: "Produtos" },
        {path: '/carrinho', label: 'Carrinho'},
    ];

    return (
        <div>
            <Headers links={links} />
        <div className={style.pedidospage}>
            {posts.length === 0 ? (
                <p>Vazio...</p>
            ) : (
                posts.map((post) => (
                    <div key={post.id}>
                        <Link to={`/pedido/${post.id}`}>
                        <p>ID: {post.id}</p> </Link>
                        <p>E-mail: {post.email}</p>
                        <p>Criado em: {new Date(post.data_pedido).toLocaleDateString()}</p>
                        <p>Preço: {post.total}</p>
                        <p>Status de Entrega: {post.entrega_status}</p>
                    </div>
                ))
            )}
        </div>
        </div>
    );
    


}

export default PedidosPage