import axios from "axios";
import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import style from '../../style/perfilpagecss/Perfil.module.css';

function Perfil() {
    const [posts, setPosts] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const navigate = useNavigate();
    const { id } = useParams();

    const getPost = async () => {
        try {
            const tokenauth = localStorage.getItem('token');
            const res = await axios.get(`http://localhost:8000/accountapi/accounts/${id}/`, {
                headers: { 'Authorization': `Bearer ${tokenauth}` }
            });
            setPosts(res.data);
        } catch (error) {
            setError(error.response?.data.error.message || 'Erro ao carregar os dados');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        getPost();
    }, [id]);

    const handleSubmit = async (event) => {
        event.preventDefault();
        const tokenauth = localStorage.getItem('token');

        try {
            await axios.delete(`http://localhost:8000/accountapi/accounts/${id}/`, {
                headers: { 'Authorization': `Bearer ${tokenauth}` }
            });
            navigate("/login");
        } catch (err) {
            console.log(err);
            setError('Erro ao deletar a conta');
        }
    };

    if (loading) return <p>Carregando...</p>;
    if (error) return <p>Erro: {error}</p>;

    return (
        <div>
            {posts ? (
                <div className={style.perfilpage}>
                    <div key={posts.id}>
                        <h2>{posts.username}</h2>
                        <h3>{posts.email}</h3>
                        <h3>{posts.data_joined}</h3>
                        <form onSubmit={handleSubmit}>
                            <button type="submit">Deletar</button>
                        </form>
                    </div>
                </div>
            ) : (
                <p>Vazio...</p>
            )}
        </div>
    );
}

export default Perfil;
