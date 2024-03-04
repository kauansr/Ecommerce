import axios from "axios"
import { useState, useEffect } from "react"
import { useNavigate, useParams } from "react-router-dom"
import style from '../../style/pedidospagecss/Pedidopage.module.css'

function UmPedido() {

    const [posts, setPosts] = useState([])

    const navigate = useNavigate()
    const { id } = useParams()


    const getPost = async () => {

        try {

            const tokenauth = localStorage.getItem('token')
            const res = await axios.get(`http://127.0.0.1:8000/pedidoapi/pedidos/${id}`, { headers: { 'Authorization': `Bearer ${tokenauth}` } })



            setPosts(res.data)



        } catch (error) {
            console.log(error)

        }


    }


    useEffect(() => {
        getPost()
    }, [])

    const handleSubmit = data => {
        data.preventDefault()
        const tokenauth = localStorage.getItem('token')

        axios.delete(`http://127.0.0.1:8000/pedidoapi/pedidos/${id}`, { headers: { 'Authorization': `Bearer ${tokenauth}` } })
            .then((res) => { navigate("/pedidos") })
            .catch((err) => console.log(err))
    }

    return (
        <div>


            {posts.length === 0 ? <p>Vazio...</p> : (

                <div className={style.pedidospage}>
                    <div key={posts.id}>
                        <div><h2> {posts.nome_pedido}
                        </h2></div>
                        <div><h3>Status: {posts.entrega_status}</h3></div>
                        <div><h3>Destinatario: {posts.email}</h3></div>
                        <div><h3>R$: {posts.preco}</h3></div>
                        <br></br>
                        <div>
                            <form onSubmit={handleSubmit}>
                                <div><button>Cancelar</button></div>
                            </form>
                        </div><br></br>

                    </div>
                </div>

            )

            }
        </div >
    )
}

export default UmPedido