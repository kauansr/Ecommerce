import axios from "axios"
import { useState, useEffect } from "react"
import { useNavigate, useParams } from "react-router-dom"
import style from '../../style/perfilpagecss/Perfil.module.css'

function Perfil() {

    const [posts, setPosts] = useState([])

    const navigate = useNavigate()
    const { id } = useParams()


    const getPost = async () => {

        try {

            const tokenauth = localStorage.getItem('token')
            const res = await axios.get(`http://localhost:8000/accountapi/accounts/${id}/`, { headers: { 'Authorization': `Bearer ${tokenauth}` } })



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

        axios.delete(`http://127.0.0.1:8000/accountapi/accounts/${id}/`, { id: id }, { headers: { 'Authorization': `Bearer ${tokenauth}` } })
            .then((res) => { navigate("/login") })
            .catch((err) => console.log(err))
    }

    return (
        <div>


            {posts.length === 0 ? <p>Vazio...</p> : (

                <div className={style.perfilpage}>
                    <div key={posts.id}>
                        <div><h2>{posts.username}</h2></div><br></br><br></br>
                        <div><h3>{posts.email}</h3></div><br></br><br></br>
                        <div><h3>{posts.data_joined}</h3></div>
                        <br></br>
                        <div>
                            <form onSubmit={handleSubmit}>
                                <button type="submit">Deletar</button>
                            </form>
                        </div><br></br>

                    </div>
                </div>

            )

            }
        </div >
    )
}

export default Perfil