import { Router } from 'express';

import User from '../controllers/User';

const router = Router();
const user = new User();

router.post('/add', user.add);
router.post('/login', user.login);

export default router;
