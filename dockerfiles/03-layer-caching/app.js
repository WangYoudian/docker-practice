
const express = require('express');
const app = express();
const port = process.env.PORT || 8000;

app.get('/', (req, res) => {
  res.send('Layer caching demo!\n');
});

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
