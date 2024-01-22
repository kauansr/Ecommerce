import axios from 'axios'
import { useState } from 'react'
import style from '../../prepagicss/CadastrouserForm.module.css'
import { useNavigate } from 'react-router-dom'

function CadastrouserForm() {


    const data = { username: "", email: "", password: "" }
    const [dataInput, setDataInput] = useState(data)

    const handleInput = (e) => {
        setDataInput({ ...dataInput, [e.target.name]: e.target.value })
    }

    const navigate = useNavigate()
    const handleSubmit = async (e) => {
        e.preventDefault()

        try {
            await axios.post("http://127.0.0.1:8000/accountapi/accountscreateapi/", dataInput)
                .then((res) =>


                    navigate("/login")

                )
                .catch((err) => console.log(err.data))
        } catch (error) {
            console.log(error)

        }


    }



    return (
        <div className={style.cadastrouserform}>
            <div>
                <form onSubmit={handleSubmit}>
                    <input type='text' name='username' onChange={handleInput} placeholder='Insira seu Username'></input><br /><br />
                    <input type='email' name='email' onChange={handleInput} placeholder='Insira seu E-mail'></input><br /><br />
                    <input type='password' name='password' onChange={handleInput} placeholder='Insira sua senha'></input><br /><br />

                    <button type='submit'>Cadastrar</button>


                </form></div>

        </div>
    )



}

export default CadastrouserForm