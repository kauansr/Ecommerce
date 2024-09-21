import axios from 'axios'
import { useState } from 'react'
import style from '../../prepagicss/LoginForm.module.css'
import { useNavigate } from 'react-router-dom'

function LoginForm() {


    const data = { email: "", password: "" }
    const [dataInput, setDataInput] = useState(data)

    const handleInput = (e) => {
        setDataInput({ ...dataInput, [e.target.name]: e.target.value })
    }

    const navigate = useNavigate()
    const handleSubmit = async (e) => {
        e.preventDefault()

        try {
            await axios.post("http://127.0.0.1:8000/accountapi/token/", dataInput)
                .then((res) =>


                    localStorage.setItem("token", res.data['access'])


                )
                .catch((err) => console.log(err.data))
        } catch (error) {
            console.log(error)

        }

        if (localStorage.getItem("token")) {
            navigate("/produtos")
        }
        else {
            window.location.reload()
        }

    }



    return (
        <div className={style.loginform}>
            
            <div>
                <form onSubmit={handleSubmit}>
                    <input type='email' name='email' onChange={handleInput} placeholder='E-mail'></input><br /><br />
                    <input type='password' name='password' onChange={handleInput} placeholder='Password'></input><br /><br />

                    <button type='submit'>Sign-in</button>


                </form>
                <ul>
            <li>Don't have an account ?<a href="/sign-up">Sign-up</a></li>
            </ul>
                </div>

        </div>
    )



}

export default LoginForm