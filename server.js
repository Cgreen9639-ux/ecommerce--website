const express = require('express');
const app = express();
const port = 8000; // You can change the port number here

app.use(express.static('public')); // Serve static files from the 'public' directory

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html'); // Serve the main HTML file
});

app.get('/api/products', (req, res) => {
  const products = [
    { id: 1, name: 'Product 1', price: '$10', image: 'https://via.placeholder.com/150' },
    { id: 2, name: 'Product 2', price: '$20', image: 'https://via.placeholder.com/150' },
    { id: 3, name: 'Product 3', price: '$30', image: 'https://via.placeholder.com/150' },
  ];
  // ...existing code...
const port = 8000;

app.get('/api/products', (req, res) => {
  const products = [
    {id: 1, name: 'Example Product', price: 19.99}
  ];
  res.json(products);
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
// ...existing code...
  res.json(products);
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${8000}`);

});
