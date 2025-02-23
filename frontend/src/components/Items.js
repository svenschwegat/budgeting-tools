'use client';
import React, { useEffect, useState } from 'react';
import AddItem from './AddItem';
import api from '../api';

const ItemList = () => {
  const [items, setItems] = useState([]);

  const fetchItems = async () => {
    try {
      const response = await api.get('/items');
      setItems(response.data.items);
    } catch (error) {
      console.error("Error fetching items", error);
    }
  };

  const addItem = async (item) => {
    try {
      await api.post('/items', { id: 0, name: item });
      fetchItems();  // Refresh the list after adding an item
    } catch (error) {
      console.error("Error adding item", error);
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  return (
    <div>
      <ul>
        {items.map((item, index) => (
          <li key={index}>{item.name}</li>
        ))}
      </ul>
      <AddItem addItem={addItem} />
    </div>
  );
};

export default ItemList;