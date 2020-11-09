#ifndef __LOGGING__
#define __LOGGING__

#ifdef __cplusplus
extern "C"{
#endif // __cplusplus

namespace logger
{
    enum Level{
        FATAL, ERROR, WARNING, INFO, DEBUG
    };

    class log{

        private:
            unsigned char this_level = DEBUG; 
            

    };
     
}

#ifdef __cplusplus
}
#endif // __cplusplus
#endif // !__LOGGING__