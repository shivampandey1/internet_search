import axios from 'axios';

export default async function handler(req, res) {
  const referer = req.headers.referer || req.headers.referrer;
  const { body } = req;

  if (req.method !== 'POST') {
    res.status(405).json({ message: 'Method should be POST' });
    return;
  }

  if (process.env.NODE_ENV !== "development") {
    if (!referer || referer !== process.env.APP_URL) {
      res.status(401).json({ message: 'Unauthorized' });
      return;
    }
  }

  // Extract the query from the messages array
  const query = body.messages && body.messages[0] ? body.messages[0].content : undefined;

  // Log the extracted query
  console.log("Full request body, ", body)
  console.log("Sending payload:", { query: query });

  // Determine which endpoint to use: default is 'search_enabled'
  const endpoint = body.useSearchDisabled ? '/search_disabled/' : '/search_enabled/';
  const url = `http://127.0.0.1:8000${endpoint}`;

  try {
    const response = await axios.post(url, { query: query }, {
      headers: { 'Content-Type': 'application/json' }
    });
    res.status(200).json(response.data);
  } catch (error) {
    console.log('Axios error:', error.response?.data || error.message);
    res.status(500).json({ message: 'Something went wrong' });
  }
}
