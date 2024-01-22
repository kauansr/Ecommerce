import axios from "axios"
import { useState, useEffect } from "react"
import { useNavigate, useParams } from "react-router-dom"
import style from '../../style/produtospagecss/Produtos.module.css'

function UmProduto() {

    const [posts, setPosts] = useState([])

    const navigate = useNavigate()
    const { id } = useParams()


    const getPost = async () => {

        try {

            const tokenauth = localStorage.getItem('token')
            const res = await axios.get(`http://localhost:8000/productapi/produtos/${id}`, { headers: { 'Authorization': `Bearer ${tokenauth}` } })



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

        axios.post(`http://127.0.0.1:8000/pedidoapi/pedidos/`, { id: id }, { headers: { 'Authorization': `Bearer ${tokenauth}` } })
            .then((res) => { navigate("/pedidos") })
            .catch((err) => console.log(err))
    }

    return (
        <div>


            {posts.length === 0 ? <p>Vazio...</p> : (

                <div className={style.produtospage}>
                    <div key={posts.id}>
                        <div><h2> {posts.nome}
                        </h2></div>
                        <div><h3>R$: {posts.preco}</h3></div>
                        <br></br>
                        <div>
                            <form onSubmit={handleSubmit}>
                                <button type="submit">Pedir</button>
                            </form>
                        </div><br></br>

                    </div>
                </div>

            )

            }
        </div >
    )
}

export default UmProduto