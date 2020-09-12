import { configure } from 'axios-hooks';
import Axios from 'axios';

const axios = Axios.create({
  baseURL: 'http://localhost:8000/api',
});

configure({ axios });

export default axios;
