import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import style from '../../prepagicss/LoginForm.module.css';
import Header from '../header/Header.js';

function LoginForm() {
    const [dataInput, setDataInput] = useState({ email: "", password: "" });
    const navigate = useNavigate();

    const handleInput = (e) => {
        setDataInput({ ...dataInput, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!dataInput.email || !dataInput.password) {
            alert("Por favor, preencha todos os campos.");
            return;
        }

        try {
            const res = await axios.post("http://127.0.0.1:8000/accountapi/token/", dataInput);
            localStorage.setItem("token", res.data['access']);
            navigate("/produtos");
        } catch (error) {
            console.error("Erro ao fazer login:", error.response ? error.response.data : error.message);
            window.location.reload();
        }
    };

    const links = [
        { path: "/sign-up", label: "Cadastrar" },
    ];

    return (
        <div>
            <Header links={links} />
            <div className={style.loginform}>
                <form onSubmit={handleSubmit}>
                    <input type='email' name='email' onChange={handleInput} placeholder='E-mail' required />
                    <input type='password' name='password' onChange={handleInput} placeholder='Password' required />
                    <button type='submit'>Sign-in</button>
                </form>
                <ul>
                    <li>Don't have an account? <Link to="/sign-up">Sign-up</Link></li>
                </ul>
            </div>
        </div>
    );
}

export default LoginForm;