//
//  UProfile.h
//  puuten
//
//  Created by wang jialei on 12-7-12.
//  Copyright (c) 2012年 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface UProfile : NSObject
@property (assign) int userID;

- (id)initWithUserID:(int)userID;
- (NSString *)replaceUnicode:(NSString *)unicodeStr;


@end
