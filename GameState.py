from this import d
import numpy as np
class GameState():
    
    def __init__(self) -> None:
        self.board = np.array([
            ['br','bk','bb','bq','bc','bb','bk','br'],
            ['bp','bp','bp','bp','bp','bp','bp','bp'],
            ['--','--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--','--'],
            ['wp','wp','wp','wp','wp','wp','wp','wp'],
            ['wr','wk','wb','wq','wc','wb','wk','wr']        
        ])
        