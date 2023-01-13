import { Router } from 'express';

import { addUser, login } from '../controllers/user';

const router = Router();

router.post('/add', addUser);
router.post('/login', login);

export default router;
