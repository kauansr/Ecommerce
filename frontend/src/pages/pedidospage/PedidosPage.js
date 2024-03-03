import axios from 'axios'
import { useState, useEffect } from 'react'
import style from '../../style/produtospagecss/Produtos.module.css'

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

    return (

        <div className={style.produtospage}>

            {posts.length === 0 ? <p>Vazio...</p> : (
                posts.map((post) => (

                    <div key={post.id} >
                        <div><p>{post.id}</p></div>
                        <div><p>{post.nome_pedido}</p></div>
                        <div><p>Preco: {post.preco}</p></div>
                        <div><p>Status de entrega: {post.entrega_status}</p></div>
                    </div>


                ))
            )

            }

        </div>
    )


}

export default PedidosPage