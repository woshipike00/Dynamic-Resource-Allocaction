__author__ = 'pike'

from Hades import Manager
from oslo import messaging
from oslo.config import cfg
from PolicyEngine.PolicyManager import PolicyManager

CONF = cfg.CONF


class PMAManager(Manager.Manager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):

        super(PMAManager, self).__init__(*args,**kwargs)

        self.policyManager = PolicyManager()

    ########################### POLICY ##############################



    def loadPolicy(self, ctxt, host, policy):

        self.policyManager.loadPolicy(policy)
        print 'loadPolicy'
        return True


    ########################### EVENT ##############################

    def handleEvent(self, ctxt, host, event):
        #implement in derived class
        pass


class ArbiterPMAManager(PMAManager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):

        super(ArbiterPMAManager, self).__init__(service_name = 'hades_arbiterPMA_service',
                                               *args,
                                               **kwargs)

    def handleEvent(self, ctxt, host, event):
        print event
        self.policyManager.assertFact(event)
        self.policyManager.run()
        result = self.policyManager.getStdout()
        return result




if __name__ == "__main__":
    manager = ArbiterPMAManager()
    print manager.service_name
