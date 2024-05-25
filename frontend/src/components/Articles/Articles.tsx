import React, { useState, useEffect } from 'react';
import { fetchArticles, createArticle, updateArticle, deleteArticle } from '../../services/apiService';
import './Articles.css'; // Import the CSS file

interface ArticlesProps {
  onArticlesFetched: (articles: any[]) => void;
}

const Articles: React.FC<ArticlesProps> = ({ onArticlesFetched }) => {
  const [articles, setArticles] = useState<any[]>([]);
  const [newArticle, setNewArticle] = useState({ title: '', content: '', author: '' });
  const [editingArticle, setEditingArticle] = useState<any | null>(null);

  useEffect(() => {
    fetchArticles().then(fetchedArticles => {
      setArticles(fetchedArticles);
      onArticlesFetched(fetchedArticles);
    }).catch(console.error);
  }, [onArticlesFetched]);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setNewArticle({ ...newArticle, [name]: value });
  };

  const handleCreateArticle = () => {
    createArticle(newArticle).then(article => {
      const updatedArticles = [...articles, article];
      setArticles(updatedArticles);
      onArticlesFetched(updatedArticles);
      setNewArticle({ title: '', content: '', author: '' });
    }).catch(console.error);
  };

  const handleEditArticle = (article: any) => {
    setEditingArticle(article);
  };

  const handleUpdateArticle = () => {
    if (editingArticle) {
      updateArticle(editingArticle.id, editingArticle).then(updatedArticle => {
        const updatedArticles = articles.map(article => (article.id === updatedArticle.id ? updatedArticle : article));
        setArticles(updatedArticles);
        onArticlesFetched(updatedArticles);
        setEditingArticle(null);
      }).catch(console.error);
    }
  };

  const handleDeleteArticle = (id: number) => {
    deleteArticle(id).then(() => {
      const updatedArticles = articles.filter(article => article.id !== id);
      setArticles(updatedArticles);
      onArticlesFetched(updatedArticles);
    }).catch(console.error);
  };

  return (
    <div className="articles-container">
      <h1 className="articles-title">Articles</h1>
      <div className="article-form">
        <input
          type="text"
          name="title"
          placeholder="Title"
          value={newArticle.title}
          onChange={handleInputChange}
          className="article-input"
        />
        <input
          type="text"
          name="content"
          placeholder="Content"
          value={newArticle.content}
          onChange={handleInputChange}
          className="article-input"
        />
        <input
          type="text"
          name="author"
          placeholder="Author"
          value={newArticle.author}
          onChange={handleInputChange}
          className="article-input"
        />
        <button onClick={handleCreateArticle} className="article-button">Create Article</button>
      </div>
      <div className="articles-list">
        {articles.map(article => (
          <div key={article.id} className="article-card">
            <h2 className="article-card-title">{article.title}</h2>
            <p className="article-card-content">{article.content}</p>
            <small className="article-card-author">By {article.author}</small>
            <div className="article-card-actions">
              <button onClick={() => handleEditArticle(article)} className="article-button">Edit</button>
              <button onClick={() => handleDeleteArticle(article.id)} className="article-button">Delete</button>
            </div>
          </div>
        ))}
      </div>
      {editingArticle && (
        <div className="edit-article-form">
          <h2>Edit Article</h2>
          <input
            type="text"
            name="title"
            placeholder="Title"
            value={editingArticle.title}
            onChange={e => setEditingArticle({ ...editingArticle, title: e.target.value })}
            className="article-input"
          />
          <input
            type="text"
            name="content"
            placeholder="Content"
            value={editingArticle.content}
            onChange={e => setEditingArticle({ ...editingArticle, content: e.target.value })}
            className="article-input"
          />
          <input
            type="text"
            name="author"
            placeholder="Author"
            value={editingArticle.author}
            onChange={e => setEditingArticle({ ...editingArticle, author: e.target.value })}
            className="article-input"
          />
          <button onClick={handleUpdateArticle} className="article-button">Update Article</button>
        </div>
      )}
    </div>
  );
};

export default Articles;
