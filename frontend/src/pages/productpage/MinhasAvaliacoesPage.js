import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../../style/produtospagecss/MinhasAvaliacoes.module.css';
import Headers from '../../components/prepaginas/header/Header';

const MinhasAvaliacoes = () => {
    const [avaliacoes, setAvaliacoes] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchAvaliacoes = async () => {
            try {
                const tokenauth = localStorage.getItem('token');
                const res = await axios.get('http://127.0.0.1:8000/productapi/avaliacoes/', {
                    headers: { 'Authorization': `Bearer ${tokenauth}` },
                });
                setAvaliacoes(res.data);
            } catch (error) {
                console.error('Erro ao carregar as avaliações', error);
            }
        };

        fetchAvaliacoes();
    }, []);

    const editarAvaliacao = (id) => {
        navigate(`/avaliacoes/${id}`);
    };

    const deletarAvaliacao = async (id) => {
        const tokenauth = localStorage.getItem('token');
        try {
            await axios.delete(`http://127.0.0.1:8000/productapi/avaliacoes/${id}/delete`, {
                headers: { 'Authorization': `Bearer ${tokenauth}` },
            });
            alert('Avaliação deletada!');
            setAvaliacoes(avaliacoes.filter(avaliacao => avaliacao.id !== id));
        } catch (error) {
            console.error('Erro ao deletar avaliação', error);
        }
    };

    return (
        <div className="minhas-avaliacoes">
            <Headers links={[{ path: "/produtos", label: "Produtos" }, { path: "/carrinho", label: "Carrinho" }]} />
            <h2>Minhas Avaliações</h2>
            <ul>
                {avaliacoes.map(avaliacao => (
                    <li key={avaliacao.id}>
                        <div>
                            <h3>Produto: {avaliacao.produto.nome}</h3>
                            <p>{avaliacao.comentario}</p>
                            <p>Nota: {avaliacao.estrelas}</p>
                            <button onClick={() => editarAvaliacao(avaliacao.id)}>Editar</button>
                            <button className="delete" onClick={() => deletarAvaliacao(avaliacao.id)}>Deletar</button>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default MinhasAvaliacoes;