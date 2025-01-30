import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import '../../style/produtospagecss/EditarAvaliacoes.module.css'
import Headers from '../../components/prepaginas/header/Header';

const EditarAvaliacao = () => {
    const [avaliacao, setAvaliacao] = useState(null);
    const [comentario, setComentario] = useState('');
    const [nota, setNota] = useState(1);
    const { id } = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchAvaliacao = async () => {
            try {
                const tokenauth = localStorage.getItem('token');
                const res = await axios.get(`http://127.0.0.1:8000/productapi/avaliacoes/${id}/`, {
                    headers: { 'Authorization': `Bearer ${tokenauth}` },
                });
                setAvaliacao(res.data);
                setComentario(res.data.comentario);
                setNota(res.data.estrelas);
            } catch (error) {
                console.error('Erro ao carregar a avaliação', error);
            }
        };

        fetchAvaliacao();
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const tokenauth = localStorage.getItem('token');
        try {
            await axios.put(`http://127.0.0.1:8000/productapi/avaliacoes/${id}/update`, {
                comentario: comentario,
                estrelas: nota,
            }, {
                headers: { 'Authorization': `Bearer ${tokenauth}` },
            });
            alert('Avaliação atualizada!');
            navigate('/minhas-avaliacoes'); 
        } catch (error) {
            console.error('Erro ao atualizar a avaliação', error);
        }
    };

    if (!avaliacao) return <div>Carregando...</div>;

    return (
        <div className="editar-avaliacao">
            <Headers links={[{ path: "/produtos", label: "Produtos" }, { path: "/carrinho", label: "Carrinho" }]} />
            <h2>Editar Avaliação</h2>
            <form onSubmit={handleSubmit}>
                <textarea
                    value={comentario}
                    onChange={(e) => setComentario(e.target.value)}
                    placeholder="Comente sobre o produto..."
                    required
                />
                <div>
                    <label>Nota:</label>
                    <input
                        type="number"
                        value={nota}
                        onChange={(e) => setNota(Number(e.target.value))}
                        min="1"
                        max="5"
                        required
                    />
                </div>
                <button type="submit">Salvar</button>
            </form>
        </div>
    );
};

export default EditarAvaliacao;